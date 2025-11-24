from django.urls import path
from games.views import example
urlpatterns = [
    path('', example , name="Example" ),
]