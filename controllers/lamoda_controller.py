from fastapi import APIRouter
from repositories.lamoda_repository import *

router = APIRouter()


@router.get('/products')
async def get_current_products():
    cached_data = await get_cached_data()
    if cached_data:
        return cached_data
    return await get_products()


@router.get('/parse')
async def parse_products():
    return await parse()
