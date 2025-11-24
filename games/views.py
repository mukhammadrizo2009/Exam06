from django.shortcuts import render
from django.http import HttpRequest , JsonResponse

# Create your views here.

def example(request: HttpRequest) -> JsonResponse:
    return JsonResponse({})