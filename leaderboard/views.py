from django.http import JsonResponse, HttpRequest
from scores.models import Score
from games.models import Game
from players.models import Player
from django.db.models import Sum, Count

def game_leaderboard(request: HttpRequest):
    game_id = request.GET.get("game_id")
    
    if not game_id:
        return JsonResponse({"error": "game_id is required"}, status=400)
    
    scores = Score.objects.filter(game_id=game_id)
    
    if not scores.exists():
        return JsonResponse([], safe=False)
    
    players = {}
    
    for score in scores:
        player_id = score.player.id
        if player_id not in players:
            players[player_id] = {
                "player": score.player.nickname,
                "player_id": player_id,
                "country": score.player.country,
                "rating": score.player.rating,
                "points": 0,
                "wins": 0,
                "draws": 0,
                "losses": 0,
            }

        players[player_id]["points"] += score.points
        
        if score.result == "win":
            players[player_id]["wins"] += 10
        elif score.result == "draw":
            players[player_id]["draws"] += 5
        else:
            players[player_id]["losses"] += 0
            
    leaderboard = list(players.values())
    leaderboard.sort(key=lambda x: x["points"], reverse=True)

    for i, points in enumerate(leaderboard, start=1):
        points["rank"] = i
        points["rating_change"] = points["points"]

    return JsonResponse(leaderboard, safe=False)

def leaderboard_top(request: HttpRequest):
    game_id = request.GET.get("game_id")
    limit = int(request.GET.get("limit", 10))

    if limit > 50:
        limit = 50

    if not game_id:
        return JsonResponse({"error": "game_id is required"}, status=400)

    scores = Score.objects.filter(game_id=game_id)

    if not scores.exists():
        return JsonResponse([], safe=False)

    players = {}

    for score in scores:
        player_id = score.player.id
        if player_id not in players:
            players[player_id] = {
                "player": score.player.nickname,
                "player_id": player_id,
                "country": score.player.country,
                "rating": score.player.rating,
                "points": 0,
            }

        players[player_id]["points"] += score.points

    leaderboard = list(players.values())
    leaderboard.sort(key=lambda x: x["points"], reverse=True)

    top_players = leaderboard[:limit]

    return JsonResponse({
        "game_id": int(game_id),
        "game_title": Game.objects.get(id=game_id).title,
        "limit": limit,
        "total_players": len(leaderboard),
        "leaderboard": top_players
    })

def global_leaderboard(request: HttpRequest):
    country = request.GET.get("country")
    limit = int(request.GET.get("limit", 100))

    if limit > 500:
        limit = 500

    players = Player.objects.all()

    if country:
        players = players.filter(country__iexact=country)

    players = players.order_by('-rating')[:limit]

    data = []
    for i, p in enumerate(players, start=1):
        data.append({
            "rank": i,
            "player": p.nickname,
            "rating": p.rating,
            "total_games": Score.objects.filter(player=p).count()
        })

    return JsonResponse({
        "total_players": players.count(),
        "country": country,
        "leaderboard": data
    })
