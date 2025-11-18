from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .NetworkHelper import NetworkHelper

BASE_URL = "http://127.0.0.1:8001/api"
USERNAME = "admin"
PASSWORD = "12345678"

api_helper = NetworkHelper(BASE_URL, username=USERNAME, password=PASSWORD)


def player_list(request):
    players = api_helper.get_list("players")

    context = {
        'players': players,
        'api_status': 'OK' if players else 'Error or Empty'
    }
    return render(request, 'web/players_list.html', context)

def player_delete(request, player_id):
    if request.method == 'POST':
        success = api_helper.delete(player_id, "players")

        if success:
            return redirect('player_list_name')
        else:
            return HttpResponse(f"Could not delete player {player_id}.", status=500)

    return redirect('player_list_name')


def character_list(request):
    characters = api_helper.get_list("characters")

    context = {
        'characters': characters,
        'api_status': 'OK' if characters else 'Error or Empty'
    }

    return render(request, 'web/characters_list.html', context)

def character_delete(request, character_id):
    if request.method == 'POST':
        success = api_helper.delete(character_id, "characters")

        if success:
            return redirect('character_list_name')
        else:
            return HttpResponse(f"Could not delete character {character_id}.", status=500)

    return redirect('character_list_name')

