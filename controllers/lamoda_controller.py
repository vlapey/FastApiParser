from fastapi import APIRouter
from repositories.lamoda_repository import parse, get_products

router = APIRouter()


@router.get('/products')
async def get_current_products():
    return await get_products()


@router.get('/parse')
async def parse_products():
    return await parse()
