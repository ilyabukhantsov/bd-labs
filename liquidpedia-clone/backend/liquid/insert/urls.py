from django.urls import path
from .views import InsertDispatcher

urlpatterns = [
    path("<str:action>/", InsertDispatcher.as_view(), name="insert-dispatcher"),
]


