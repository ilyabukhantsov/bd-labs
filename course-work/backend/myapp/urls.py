from django.urls import path
from .views import CreateTeamAPIView, UpdateTeamAPIView, HardDeleteTeamAPIView, SoftDeletePlayerAPIView, PlayersAbove18APIView, PlayersAlphabeticalAPIView, TeamPlayersAnalyticsAPIView

urlpatterns = [
    path('create-team/', CreateTeamAPIView.as_view(), name='create-team'),
    path('update-team/', UpdateTeamAPIView.as_view(), name='update-team'),
    path('delete-team/<int:team_id>/', HardDeleteTeamAPIView.as_view(), name='delete-team'),
    path('soft-delete-player/<int:player_id>/', SoftDeletePlayerAPIView.as_view(), name='soft-delete-player'),
    path("players-by-age/", PlayersAbove18APIView.as_view()),
    path("players-by-abc/", PlayersAlphabeticalAPIView.as_view()),
]
