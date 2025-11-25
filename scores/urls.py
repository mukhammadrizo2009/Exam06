from django.urls import path
from . import views

urlpatterns = [
    path('', views.scores_list, name="scores-list"),
    path('<int:id>/', views.score_detail, name="scores-detail"),
]
