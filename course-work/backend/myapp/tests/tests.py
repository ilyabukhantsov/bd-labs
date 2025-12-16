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
    def test_basic_url_reverse_and_get(self):
        response = self.client.get('/')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

@patch('myapp.views.create_team_with_roster')
class CreateTeamAPITest(APITestCase):
    url = reverse('create-team') 

    def test_create_team_dummy_check(self, mock_create_team):
        mock_create_team.return_value = {"error": "Mocked Service Error"}
        response = self.client.post(self.url, {}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("обязательны", response.data['error'])




@patch('myapp.views.create_team_with_roster')
class CreateTeamAPITest(APITestCase):
    url = reverse('create-team') 

    def test_01_create_team_success(self, mock_create_team):
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
        data = {"team_name": "Missing Data Team"}
        
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("обязательны", response.data['error'])
        mock_create_team.assert_not_called()
        
    def test_03_create_team_service_failure(self, mock_create_team):
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
        data = {"new_team_name": "Test"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("team_id обязательный", response.data['error'])


@patch('myapp.views.hard_delete_team')
class HardDeleteTeamAPITest(APITestCase):
    def test_06_delete_team_success(self, mock_delete_team):
        team_id = 10
        url = reverse('delete-team', kwargs={'team_id': team_id})
        mock_delete_team.return_value = {"message": f"Team {team_id} hard deleted"}

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_delete_team.assert_called_once_with(team_id)


@patch('myapp.views.soft_delete_player')
class SoftDeletePlayerAPITest(APITestCase):
    def test_07_soft_delete_success(self, mock_soft_delete):
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
        
        mock_update_team.return_value = {"error": "Team not found"}
        
        data = {"team_id": 999, "new_team_name": "Test"}
        
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Team not found", response.data['error'])
        
    def test_07_update_team_validation_failure(self, mock_update_team):
        mock_update_team.return_value = {"error": "Validation error", "details": "end_date must be greater than start_date"}
        
        data = {"team_id": 1, "roster_updates": {"roster_id": 1, "start_date": "2025-01-01", "end_date": "2024-01-01"}}
        
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Validation error", response.data['error'])


@patch('myapp.views.hard_delete_team')
class HardDeleteTeamAPITest(APITestCase):

    def test_08_delete_team_not_found(self, mock_delete_team):
        team_id = 999
        url = reverse('delete-team', kwargs={'team_id': team_id})
        
        mock_delete_team.return_value = {"error": "Team not found"}

        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Team not found", response.data['error'])

    def test_09_delete_team_integrity_error(self, mock_delete_team):
        team_id = 1
        url = reverse('delete-team', kwargs={'team_id': team_id})
        
        mock_delete_team.return_value = {"error": "Integrity error", "details": "Cannot delete because of FK constraint"}

        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Integrity error", response.data['error'])


@patch('myapp.views.soft_delete_player')
class SoftDeletePlayerAPITest(APITestCase):

    def test_10_soft_delete_player_not_found(self, mock_soft_delete):
        player_id = 999
        url = reverse('soft-delete-player', kwargs={'player_id': player_id})
        
        mock_soft_delete.return_value = {"error": "Player not found"}

        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Player not found", response.data['error'])

#Rollback test
class CreateTeamRollbackTests(APITestCase):
    def test_create_team_rollback_on_player_error(self):

        url = "/api/create-team/"

        payload = {
            "team_name": "RollbackTeam",
            "roster_start_date": "2025-01-01",
            "players": [
                {
                    "nick": "valid_player",
                    "age": 20
                },
                {
                    "age": 17
                }
            ]
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)

        self.assertEqual(Team.objects.count(), 0)
        self.assertEqual(Roster.objects.count(), 0)
        self.assertEqual(Player.objects.count(), 0)