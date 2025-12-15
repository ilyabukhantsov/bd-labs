from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch
from django.db import connection
from datetime import date
from myapp.team.service import create_team_with_roster

from django.db import IntegrityError 
from django.core.exceptions import ValidationError



from ..models import Team, Roster, Player

class BasicSanityTest(APITestCase):
    """
    Простейший тест для проверки, что тестовая среда Docker работает
    и может обрабатывать базовые запросы.
    """
    
    def test_basic_url_reverse_and_get(self):
        """Проверяет, что корневой путь (/) возвращает 404 (но не ошибку сервера)."""
        response = self.client.get('/')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

@patch('myapp.views.create_team_with_roster')
class CreateTeamAPITest(APITestCase):
    """
    Проверяем, что даже если сервис заглушен, маршрут резолвится.
    """
    url = reverse('create-team') 

    def test_create_team_dummy_check(self, mock_create_team):
        """Проверяет только резолвинг URL и метод POST без данных."""
        mock_create_team.return_value = {"error": "Mocked Service Error"}
        response = self.client.post(self.url, {}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("обязательны", response.data['error'])




@patch('myapp.views.create_team_with_roster')
class CreateTeamAPITest(APITestCase):
    url = reverse('create-team') 

    def test_01_create_team_success(self, mock_create_team):
        """Проверка успешного создания команды (HTTP 201)."""
        mock_create_team.return_value = {"team_id": 1, "message": "Team created"}

        data = {
            "team_name": "Test Team Alpha",
            "roster_start_date": "2025-01-01",
            "players": [{"nick": "P1", "age": 25}]
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("team_id", response.data)
        mock_create_team.assert_called_once()

    def test_02_create_team_missing_required_field(self, mock_create_team):
        """Проверка ошибки при отсутствии обязательных полей (HTTP 400)."""
        data = {"team_name": "Missing Data Team"}
        
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("обязательны", response.data['error'])
        mock_create_team.assert_not_called()
        
    def test_03_create_team_service_failure(self, mock_create_team):
        """Проверка возврата ошибки от сервисной функции (HTTP 400)."""
        mock_create_team.return_value = {"error": "DB integrity error"}

        data = {
            "team_name": "Invalid Team",
            "roster_start_date": "2025-01-01",
            "players": [{"nick": "P1", "age": 25}]
        }
        
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)


@patch('myapp.views.update_team_and_roster')
class UpdateTeamAPITest(APITestCase):
    url = reverse('update-team')

    def test_04_update_team_success(self, mock_update_team):
        """Проверка успешного обновления команды (HTTP 200)."""
        mock_update_team.return_value = {"team_id": 1, "message": "Team updated successfully"}
        
        data = {
            "team_id": 1,
            "new_team_name": "New Team Name"
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_update_team.assert_called_once_with(
            team_id=1,
            new_team_name="New Team Name",
            new_logo_bytes=None,
            roster_updates=None
        )
        
    def test_05_update_team_missing_id(self, mock_update_team):
        """Проверка ошибки при отсутствии team_id (HTTP 400)."""
        data = {"new_team_name": "Test"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("team_id обязательный", response.data['error'])


@patch('myapp.views.hard_delete_team')
class HardDeleteTeamAPITest(APITestCase):
    def test_06_delete_team_success(self, mock_delete_team):
        """Проверка успешного жесткого удаления (HTTP 200)."""
        team_id = 10
        url = reverse('delete-team', kwargs={'team_id': team_id})
        mock_delete_team.return_value = {"message": f"Team {team_id} hard deleted"}

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_delete_team.assert_called_once_with(team_id)


@patch('myapp.views.soft_delete_player')
class SoftDeletePlayerAPITest(APITestCase):
    def test_07_soft_delete_success(self, mock_soft_delete):
        """Проверка успешного мягкого удаления игрока (HTTP 200)."""
        player_id = 5
        url = reverse('soft-delete-player', kwargs={'player_id': player_id})
        mock_soft_delete.return_value = {"message": f"Player {player_id} soft deleted"}

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_soft_delete.assert_called_once_with(player_id)








@patch('myapp.views.update_team_and_roster')
class UpdateTeamAPITest(APITestCase):
    url = reverse('update-team')


    def test_06_update_team_not_found(self, mock_update_team):
        """Проверка возврата ошибки, если команда не найдена (Team not found)."""
        
        mock_update_team.return_value = {"error": "Team not found"}
        
        data = {"team_id": 999, "new_team_name": "Test"}
        
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Team not found", response.data['error'])
        
    def test_07_update_team_validation_failure(self, mock_update_team):
        """Проверка возврата ошибки при нарушении валидации (например, неправильные даты ростера)."""
        
        mock_update_team.return_value = {"error": "Validation error", "details": "end_date must be greater than start_date"}
        
        data = {"team_id": 1, "roster_updates": {"roster_id": 1, "start_date": "2025-01-01", "end_date": "2024-01-01"}}
        
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Validation error", response.data['error'])


@patch('myapp.views.hard_delete_team')
class HardDeleteTeamAPITest(APITestCase):

    def test_08_delete_team_not_found(self, mock_delete_team):
        """Проверка возврата ошибки, если команда не найдена при удалении."""
        team_id = 999
        url = reverse('delete-team', kwargs={'team_id': team_id})
        
        mock_delete_team.return_value = {"error": "Team not found"}

        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Team not found", response.data['error'])

    def test_09_delete_team_integrity_error(self, mock_delete_team):
        """Проверка обработки IntegrityError (например, при наличии связанных записей)."""
        team_id = 1
        url = reverse('delete-team', kwargs={'team_id': team_id})
        
        mock_delete_team.return_value = {"error": "Integrity error", "details": "Cannot delete because of FK constraint"}

        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Integrity error", response.data['error'])


@patch('myapp.views.soft_delete_player')
class SoftDeletePlayerAPITest(APITestCase):

    def test_10_soft_delete_player_not_found(self, mock_soft_delete):
        """Проверка возврата ошибки, если игрок не найден при мягком удалении."""
        player_id = 999
        url = reverse('soft-delete-player', kwargs={'player_id': player_id})
        
        mock_soft_delete.return_value = {"error": "Player not found"}

        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Player not found", response.data['error'])