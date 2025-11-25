from django.urls import path
from .views import game_leaderboard , leaderboard_top , global_leaderboard

urlpatterns = [
    path('', game_leaderboard, name='GameLeaderboard'),
    path('top/', leaderboard_top, name="TopLederboard"),
    path('global/', global_leaderboard, name='GlobalLeaderboard'),
]