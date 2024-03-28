from os import getenv
from dotenv import load_dotenv
import redis.asyncio as redis
import motor.motor_asyncio


load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(getenv('CLIENT'))
db = client[getenv('DB')]

REDIS_HOST = getenv('REDIS_HOST')
REDIS_PORT = getenv('REDIS_PORT')

redis_pool = redis.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}')


class LamodaMongoConnection:
    collection = db['goods']


class TwitchMongoConnection:
    collection_streamers = db['streamers']
    collection_games = db['games']
