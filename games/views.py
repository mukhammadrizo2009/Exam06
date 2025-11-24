import json 

from django.shortcuts import render
from django.http import HttpRequest , JsonResponse
from .models import Game

def game_list_create(request: HttpRequest):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        
        game = Game.objects.create(
            title=data.get('title'),
            location=data.get('location'),
            start_date=data.get('start_date'),
            description=data.get('description'),
        )
        
        return JsonResponse({
            "id": game.id,
            "title": game.title,
            "location": game.location,
            "start_date": str(game.start_date),
            "description": game.description,
            "created_at": game.created_at.isoformat()
        }, status=201)
    
    return JsonResponse({"error": "Method not allowed"}, status=405)

def game_detail(request: HttpRequest , id):
    try:
        game = Game.objects.get(id=id)
    except Game.DoesNotExist:
        return JsonResponse({"error": "Game not found"}, status=404)
    
    if request.method == "GET":
        return JsonResponse({
            "id": game.id,
            "title": game.title,
            "location": game.location,
            "start_date": str(game.start_date),
            "description": game.description,
            "created_at": game.created_at.isoformat()
        })
    
    if request.method == "PATCH":
        data = json.loads(request.body.decode('utf-8'))
        
        if "description" in data:
            game.description = data['description']
            
        if "title" in data:
            game.title = data["title"]
            
        if "location" in data:
            game.location = data["location"]
            
        if "start_date" in data:
            game.start_date = data["start_date"]
            
        game.save()
        
        return JsonResponse({"message": "Game updated successfully..!"})
    
    if request.method == "DELETE":
        game.delete()
        return JsonResponse({"message": "Game deleted successfully..!"})
    
    return JsonResponse({"error": "Method not allowed"}, status=405)