import os
from auth.twitch_auth import get_access_token
import requests
from os import getenv
from dotenv import load_dotenv

load_dotenv()
twitch_scraper_url = getenv('TWITCH_SCRAPER_URL')


def get_streamed_games_json() -> dict:
    headers = {
        'Client-ID': os.getenv('TWITCH_CLIENT_ID'),
        'Authorization': f'Bearer {get_access_token()}'
    }
    params = {
        'first': 100,
    }

    response = requests.get(twitch_scraper_url, headers=headers, params=params)
    data = response.json()
    return data


def get_streamers_json() -> dict:
    headers = {
        "Client-ID": os.getenv('TWITCH_CLIENT_ID'),
        "Authorization": f"Bearer {get_access_token()}"
    }
    params = {
        "first": 100,
    }

    response = requests.get(twitch_scraper_url, headers=headers, params=params)
    data = response.json()
    return data


def get_streamed_games_list(data) -> list:
    unique_games = []
    games = []
    for stream in data['data']:
        game_name = stream['game_name']
        if game_name not in unique_games:
            unique_games.append(game_name)
            games.append(game_name)
    return games


def get_streamers_list(data) -> list:
    streamers = []
    for stream in data["data"]:
        streamers.append(stream["user_name"])
    return streamers
