from fastapi import APIRouter
import requests
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()


TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
TWITCH_CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')
url = "https://api.twitch.tv/helix/streams"


@router.get('/names')
def get_streamed_games():
    headers = {
        'Client-ID': TWITCH_CLIENT_ID,
        'Authorization': f'Bearer {get_access_token()}'
    }
    params = {
        'first': 100,
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    unique_games = []
    games = []
    for stream in data['data']:
        game_name = stream['game_name']
        if game_name not in unique_games:
            unique_games.append(game_name)
            games.append(game_name)
    return set(games)


@router.get("/streamers")
def get_streamer_nicknames():
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {get_access_token()}"
    }
    params = {
        "first": 100,
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    streamers = []
    for stream in data["data"]:
        streamers.append(stream["user_name"])

    return streamers


def get_access_token():
    params = {
        'client_id': TWITCH_CLIENT_ID,
        'client_secret': TWITCH_CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }

    response = requests.post(url, params=params)
    data = response.json()
    return data['access_token']

