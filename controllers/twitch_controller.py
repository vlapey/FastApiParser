from fastapi import APIRouter
from repositories.twitch_repository import *

router = APIRouter()

TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
TWITCH_CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')


@router.get('/games')
def get_streamed_games():
    data = get_streamed_games_json()
    return get_streamed_games_list(data)


@router.get("/streamers")
def get_streamer_nicknames():
    data = get_streamers_json()
    return get_streamers_list(data)
