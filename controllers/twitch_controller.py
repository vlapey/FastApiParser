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
    data = await get_streamed_games_json()
    return await get_streamed_games_list(data)


@router.get("/streamers")
async def get_streamer_nicknames():
    data = await get_streamers_json()
    return await get_streamers_list(data)

