import json
from django.http import HttpRequest , JsonResponse
from django.db.models import Q
from .models import Player

def player_list_create(request: HttpRequest):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        
        nickname = data.get("nickname")
        country = data.get("country")
        
        if Player.objects.filter(nickname=nickname).exists():
            return JsonResponse({"error": "Nickname must be unique..!"}, status=400)
        
        player = Player.objects.create(
            nickname=nickname,
            country=country
        )
        
        return JsonResponse({
            "id": player.id,
            "nickname": player.nickname,
            "country":player.country,
            "rating": player.rating,
            "created_at": player.created_at.isoformat()
        }, status=201)
        
    if request.method == "GET":
        players = Player.objects.all()
        
        country = request.GET.get("country")
        min_rating = request.GET.get("min_rating")
        search = request.GET.get("search")
        
        if country:
            players = players.filter(country__iexact=country)
            
        if min_rating:
            players = players.filter(rating_gte=min_rating)
            
        if search:
            players = players.filter(nickname__icontains=search)
            
        results = []
        
        for player in players:
            results.append({
                "id": player.id,
                "nickname": player.nickname,
                "country": player.country,
                "rating": player.rating,
                "created_at": player.created_at.isoformat()
                })
            return JsonResponse({
                "count": players.count(),
                "next": None,
                "previous": None,
                "results": results
            }, status=200)
            
        return JsonResponse({"error": "Method not allowed..!"}, status=405)
def player_detail(request: HttpRequest, id):
    try:
        player = Player.objects.get(id=id)
    except Player.DoesNotExist:
        return JsonResponse({"error": "Player not found..!"}, status=404)
    if request.method == "GET":
        return JsonResponse({
            "id": player.id,
            "nickname": player.nickname,
            "country":player.country,
            "rating":player.rating,
            "created_at": player.created_at.isoformat()
            })
        
    if request.method == "PATCH":
        data = json.loads(request.body.decode("utf-8"))
        
        if "country" in data:
            player.country = data["country"]
            
        if "nickname" in data:
            if Player.objects.exclude(id=player.id).filter(nickname=data["nickname"]).exists():
                return JsonResponse({"error": "Nickname must be unique..!"}, status=400)
            player.nickname = data["nickname"]
            
        player.save()
        return JsonResponse({"message": "Player updated successfully"})
    
    if request.method == "DELETE":
        player.delete()
        return JsonResponse({"message": "Player deleted successfully..!"})
    
    return JsonResponse({"error": "Method not allowed..!"}, status=405)