from fastapi import APIRouter, Depends, HTTPException
from prisma.models import Product

from src.db import prisma
from src.utils.auth import get_current_user

router = APIRouter

@router.post('/products')
async def create_product(product:dict,current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=400, detail="User Does not exist")

    if current_user.role != "ADMIN":
        raise HTTPException(status_code=401, detail="Only Admin can create products")

