from django.urls import path
from scores.views import example

urlpatterns = [
    path('', example , name="Example" ),
]