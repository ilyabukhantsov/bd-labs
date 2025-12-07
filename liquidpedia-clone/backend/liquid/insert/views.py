from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class InsertDispatcher(APIView):

    def post(self, request, action):

        actions = {
            "add_team": self.add_team,
            "add_roster": self.add_roster,
            "sync_prizes": self.sync_prizes,
        }

        if action not in actions:
            return Response({"error": "Unknown action"}, status=404)

        return actions[action](request)

    def add_team(self, request):
        name = request.data.get("name")
        region = request.data.get("region")

        from tournaments.models import Team
        team = Team.objects.create(name=name, region=region)

        return Response({"status": "OK", "team_id": team.id})

    def add_roster(self, request):
        return Response({"status": "Added roster"})

    def sync_prizes(self, request):
        return Response({"status": "Prizes synced"})
