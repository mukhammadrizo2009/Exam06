import json
from django.http import JsonResponse , HttpRequest , HttpResponseNotAllowed
from .models import Score
from games.models import Game
from players.models import Player

def scores_list(request: HttpRequest):
    if request.method == "GET":
        game_id = request.GET.get('game_id')
        player_id = request.GET.get('player_id')
        result = request.GET.get('result')
        
        scores = Score.objects.all()
        
        if game_id:
            scores = scores.filter(game_id=game_id)
        if player_id:
            scores = scores.filter(player_id=player_id)
        if result:
            scores = scores.filter(result=result)

        data = []
        for score in scores:
            data.append({
                "id": score.id,
                "game": {"id": score.game.id, "title": score.game.title},
                "player": {"id": score.player.id, "nickname": score.player.nickname},
                "result": score.result,
                "points": score.points,
                "opponent_name": score.opponent_name,
                "created_at": score.created_at.isoformat(),
            })
            
        return JsonResponse({"count": len(data), "results": data})
    
    elif request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))
        game = Game.objects.get(id=body["game"])
        player = Player.objects.get(id=body["player"])

        score = Score.objects.create(
            game=game,
            player=player,
            result=body["result"],
            opponent_name=body["opponent_name"]
        )
        
        return JsonResponse({
            "id": score.id,
            "game": {"id": game.id, "title": game.title},
            "player": {"id": player.id, "nickname": player.nickname},
            "result": score.result,
            "points": score.points,
            "opponent_name": score.opponent_name,
            "created_at": score.created_at.isoformat(),
        }, status=201)

    return HttpResponseNotAllowed(["GET", "POST"])

def score_detail(request: HttpRequest, id):
    try:
        score = Score.objects.get(id=id)
        
    except Score.DoesNotExist:
        
        return JsonResponse({"error": "Score not found"}, status=404)

    if request.method == "GET":
        return JsonResponse({
            "id": score.id,
            "game": {
                "id": score.game.id,
                "title": score.game.title,
                "location": score.game.location,
            },
            "player": {
                "id": score.player.id,
                "nickname": score.player.nickname,
                "country": score.player.country,
            },
            "result": score.result,
            "points": score.points,
            "opponent_name": score.opponent_name,
            "created_at": score.created_at.isoformat(),
        })

    elif request.method == "DELETE":
        score.delete()
        return JsonResponse({}, status=204)

    return HttpResponseNotAllowed(["GET", "DELETE"])