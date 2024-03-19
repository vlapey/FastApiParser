from fastapi import APIRouter
from lamoda_repositories.repository import parse, get_products

router = APIRouter()


@router.get('/products')
def get_current_products():
    return get_products()


@router.get('/parse')
def parse_products():
    return parse()
