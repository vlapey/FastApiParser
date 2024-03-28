from os import getenv
import motor.motor_asyncio
from dotenv import load_dotenv
import aioredis

load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(getenv('CLIENT'))
db = client[getenv('DB')]

REDIS_HOST = getenv('REDIS_HOST')
REDIS_PORT = getenv('REDIS_PORT')

redis_pool = aioredis.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}')


class LamodaDbConnection:
    collection = db['goods']


class TwitchDbConnection:
    collection_streamers = db['streamers']
    collection_games = db['games']