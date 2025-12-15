from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date

from myapp.models import Team, Roster, Player, RosterPlayer

API_PREFIX = "/api"


class OLAPRoutingTest(APITestCase):

    def test_players_above_18_endpoint(self):
        response = self.client.get(f"{API_PREFIX}/players-by-age/")
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_players_alphabetical_endpoint(self):
        response = self.client.get(f"{API_PREFIX}/players-by-abc/")
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class OLAPDataTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.team_a = Team.objects.create(name="Team Alpha")
        cls.team_b = Team.objects.create(name="Team Beta")

        cls.roster_a = Roster.objects.create(
            team=cls.team_a,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
        )

        cls.roster_b = Roster.objects.create(
            team=cls.team_b,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
        )

        cls.alice = Player.objects.create(nick="Alice", age=25)
        cls.bob = Player.objects.create(nick="Bob", age=30)
        cls.charlie = Player.objects.create(nick="Charlie", age=16)
        cls.dave = Player.objects.create(nick="Dave", age=22)

        RosterPlayer.objects.create(player=cls.alice, roster=cls.roster_a)
        RosterPlayer.objects.create(player=cls.bob, roster=cls.roster_a)
        RosterPlayer.objects.create(player=cls.charlie, roster=cls.roster_b)
        RosterPlayer.objects.create(player=cls.dave, roster=cls.roster_b)


    def test_players_above_18_only(self):
        response = self.client.get(f"{API_PREFIX}/players-by-age/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ages = [p["age"] for p in response.data]
        self.assertTrue(all(age > 18 for age in ages))

    def test_players_above_18_sorted(self):
        response = self.client.get(f"{API_PREFIX}/players-by-age/")
        ages = [p["age"] for p in response.data]
        self.assertEqual(ages, sorted(ages))

    def test_players_sorted_alphabetically(self):
        response = self.client.get(f"{API_PREFIX}/players-by-abc/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        nicks = [p["nick"] for p in response.data]
        self.assertEqual(nicks, sorted(nicks))
