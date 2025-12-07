from django.urls import path
from .views import TournamentListView, TournamentInsertView, TournamentDeleteView

urlpatterns = [
    path("tournaments/", TournamentListView.as_view()),
    path("tournaments/insert/", TournamentInsertView.as_view()),
    path("delete/<int:tournament_id>/", TournamentDeleteView.as_view()),
]
