from django.urls import path
from .views import (
    TournamentListCreateView,
    TournamentDetailView,
    PlayerListCreateView,
    PlayerDetailView,
)

urlpatterns = [
    path('tournaments/', TournamentListCreateView.as_view(), name='tournament-list'),
    path('tournaments/<int:pk>/', TournamentDetailView.as_view(), name='tournament-detail'),

    path('players/', PlayerListCreateView.as_view(), name='player-list'),
    path('players/<int:pk>/', PlayerDetailView.as_view(), name='player-detail'),
]
