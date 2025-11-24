from django.urls import path
from games.views import game_list_create , game_detail

urlpatterns = [
    path('', game_list_create, name="GameList"),
    path('<int:id>/', game_detail, name="GameDetail")
]