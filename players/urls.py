from django.urls import path
from players.views import player_list_create , player_detail

urlpatterns = [
    path('', player_list_create, name="PlayerList"),
    path('<int:id>/', player_detail, name="PlayerDetail")
]