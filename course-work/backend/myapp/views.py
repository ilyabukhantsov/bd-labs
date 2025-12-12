from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .team.service import create_team_with_roster
from .team.service import update_team_and_roster
from .team.service import hard_delete_team
from .team.service import soft_delete_player

class CreateTeamAPIView(APIView):
    """
    Создание команды с ростером, игроками и активным ростером
    """

    def post(self, request):
        data = request.data

        team_name = data.get("team_name")
        logo_bytes = data.get("logo_bytes")  # можно Base64
        roster_start_date = data.get("roster_start_date")
        roster_end_date = data.get("roster_end_date", None)
        players_data = data.get("players", [])

        if not team_name or not roster_start_date or not players_data:
            return Response({"error": "team_name, roster_start_date и players обязательны"}, status=status.HTTP_400_BAD_REQUEST)

        result = create_team_with_roster(
            team_name=team_name,
            logo_bytes=logo_bytes,
            players_data=players_data,
            roster_start_date=roster_start_date,
            roster_end_date=roster_end_date
        )

        if "error" in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=status.HTTP_201_CREATED)

class UpdateTeamAPIView(APIView):
    """
    Обновление команды, её ростера и игроков
    """

    def post(self, request):
        data = request.data
        team_id = data.get("team_id")
        if not team_id:
            return Response({"error": "team_id обязательный"}, status=status.HTTP_400_BAD_REQUEST)

        result = update_team_and_roster(
            team_id=team_id,
            new_team_name=data.get("new_team_name"),
            new_logo_bytes=data.get("new_logo_bytes"),
            roster_updates=data.get("roster_updates")
        )

        if "error" in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=status.HTTP_200_OK)


class HardDeleteTeamAPIView(APIView):
    def delete(self, request, team_id):
        result = hard_delete_team(team_id)
        if "error" in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        return Response(result, status=status.HTTP_200_OK)

class SoftDeletePlayerAPIView(APIView):
    def delete(self, request, player_id):
        result = soft_delete_player(player_id)
        if "error" in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        return Response(result, status=status.HTTP_200_OK)