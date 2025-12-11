from rest_framework import generics
from .models import Tournament, Player
from .serializers import TournamentSerializer, PlayerSerializer


# -----------------------------
# Tournament Views
# -----------------------------

# GET (list) + POST (create)
class TournamentListCreateView(generics.ListCreateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer


# GET (single) + PUT/PATCH (update) + DELETE
class TournamentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer


# -----------------------------
# Player Views
# -----------------------------

# GET list players + POST create player
class PlayerListCreateView(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


# GET one player + UPDATE + DELETE
class PlayerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
