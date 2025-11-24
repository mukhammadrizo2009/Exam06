from django.urls import path
from leaderboard.views import example

urlpatterns = [
    path('', example , name="Example" ),
]