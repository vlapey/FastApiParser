import requests
import os
from dotenv import load_dotenv

load_dotenv()


def get_access_token() -> str:

    url = "https://id.twitch.tv/oauth2/token"

    params = {
        'client_id': os.getenv('TWITCH_CLIENT_ID'),
        'client_secret': os.getenv('TWITCH_CLIENT_SECRET'),
        'grant_type': 'client_credentials'
    }

    response = requests.post(url, params=params)
    data = response.json()
    return data['access_token']
