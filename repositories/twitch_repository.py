import os

from auth.twitch_auth import get_access_token
from os import getenv
from dotenv import load_dotenv
from persistence.db_conn import TwitchMongoConnection, redis_pool
import aiohttp
import pickle

load_dotenv()
twitch_scraper_url = getenv('TWITCH_SCRAPER_URL')


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

    await TwitchMongoConnection.collection_games.insert_many(games)
    return await get_data(0)


async def get_streamers_list(data) -> list:
    streamers = []
    for stream in data["data"]:
        info = {
            'streamer_name': stream['user_name'],
            'viewer_count': stream['viewer_count']
        }
        streamers.append(info)
    await TwitchMongoConnection.collection_streamers.insert_many(streamers)
    return await get_data(1)


async def get_data(selector):
    if selector:
        streamers = await TwitchMongoConnection.collection_streamers.find({}, {"_id": False}).to_list(length=None)
        return streamers

    games = await TwitchMongoConnection.collection_games.find({}, {"_id": False}).to_list(length=None)
    return games


async def cache_data(some_list, selector) -> list:
    await redis_pool.set(selector, pickle.dumps(some_list), ex=os.getenv('DEFAULT_CACHE_EXPIRATION'))
    await redis_pool.aclose()

    return some_list


async def get_cached_data(selector):

    cashed_data = await redis_pool.get(selector)

    await redis_pool.aclose()

    if cashed_data:
        return pickle.loads(cashed_data)

    return None
