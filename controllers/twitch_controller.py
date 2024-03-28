from fastapi import APIRouter
from repositories.twitch_repository import *
from os import getenv
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

TWITCH_CLIENT_ID = getenv('TWITCH_CLIENT_ID')
TWITCH_CLIENT_SECRET = getenv('TWITCH_CLIENT_SECRET')


@router.get('/games')
async def get_streamed_games():
    selector = 'games'
    cached_data = await get_cached_data(selector)
    if cached_data:
        return cached_data

    data = await get_streamed_games_json()
    game_list = await get_streamed_games_list(data)
    return await cache_data(game_list, selector)


@router.get("/streamers")
async def get_streamers():
    selector = 'streamers'
    cached_data = await get_cached_data(selector)
    if cached_data:
        return cached_data

    data = await get_streamers_json()
    streamers_list = await get_streamers_list(data)
    return await cache_data(streamers_list, selector)

