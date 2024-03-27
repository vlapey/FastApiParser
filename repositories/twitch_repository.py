import aiohttp
import motor.motor_asyncio
from auth.twitch_auth import get_access_token
from os import getenv
from dotenv import load_dotenv

load_dotenv()
twitch_scraper_url = getenv('TWITCH_SCRAPER_URL')

client = motor.motor_asyncio.AsyncIOMotorClient(getenv('CLIENT'))
db = client[getenv('DB')]
collection_streamers = db['streamers']
collection_games = db['games']


async def get_streamed_games_json() -> dict:
    headers = {
        'Client-ID': getenv('TWITCH_CLIENT_ID'),
        'Authorization': f'Bearer {get_access_token()}'
    }
    params = {
        'first': 100,
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(twitch_scraper_url, headers=headers, params=params) as response:
            data = await response.json()
            return data


async def get_streamers_json() -> dict:
    headers = {
        "Client-ID": getenv('TWITCH_CLIENT_ID'),
        "Authorization": f"Bearer {get_access_token()}"
    }
    params = {
        "first": 100,
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(twitch_scraper_url, headers=headers, params=params) as response:
            data = await response.json()
            return data


async def get_streamed_games_list(data) -> list:
    unique_games = []
    games = []
    for stream in data['data']:
        game_name = stream['game_name']
        if game_name not in unique_games:
            unique_games.append(game_name)
            game = {
                'game_name': game_name,
                'viewer_count': stream['viewer_count']
            }
            games.append(game)

    await collection_games.insert_many(games)
    return await get_data(0)


async def get_streamers_list(data) -> list:
    streamers = []
    for stream in data["data"]:
        info = {
            'streamer_name': stream['user_name'],
            'viewer_count': stream['viewer_count']
        }
        streamers.append(info)
    await collection_streamers.insert_many(streamers)
    return await get_data(1)


async def get_data(selector):
    if selector:
        streamers = await collection_streamers.find({}, {"_id": False}).to_list(length=None)
        return streamers
    games = await collection_games.find({}, {"_id": False}).to_list(length=None)
    return games
