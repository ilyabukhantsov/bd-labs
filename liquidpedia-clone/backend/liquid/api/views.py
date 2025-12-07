from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import Tournament
from .serializers import TournamentSerializer
from rest_framework import status

class TournamentListView(APIView):
    def get(self, request):
        tournaments = Tournament.objects.all()   # ← ВЗЯТЬ ДАННЫЕ ИЗ SQLite
        serializer = TournamentSerializer(tournaments, many=True)
        return Response(serializer.data)

from core.models import Tournament
from .serializers import TournamentSerializer, TournamentCreateSerializer


class TournamentInsertView(APIView):
    def post(self, request):
        serializer = TournamentCreateSerializer(data=request.data)
        if serializer.is_valid():
            tournament = serializer.save()
            return Response(
                TournamentSerializer(tournament).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TournamentDeleteView(APIView):
    def delete(self, request, tournament_id):
        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except Tournament.DoesNotExist:
            return Response(
                {"error": "Tournament not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        tournament.delete()
        return Response(
            {"message": "Tournament deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )