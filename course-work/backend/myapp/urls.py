from django.urls import path
from .views import CreateTeamAPIView, UpdateTeamAPIView, HardDeleteTeamAPIView, SoftDeletePlayerAPIView

urlpatterns = [
    path('create-team/', CreateTeamAPIView.as_view(), name='create-team'),
    path('update-team/', UpdateTeamAPIView.as_view(), name='update-team'),
    path('delete-team/<int:team_id>/', HardDeleteTeamAPIView.as_view(), name='delete-team'),
    path('soft-delete-player/<int:player_id>/', SoftDeletePlayerAPIView.as_view(), name='soft-delete-player'),
]
