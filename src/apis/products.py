from typing import List

from fastapi import APIRouter, Depends, HTTPException

from src.db import prisma
from src.models.schema import ProductIn, ProductOut
from src.utils.auth import get_current_user
from src.utils.cloudinary_config import upload_image

router = APIRouter()

@router.post("/", response_model=ProductOut)
async def create_product(product:ProductIn,current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=400, detail="User Does not exist")

    if current_user.role != "ADMIN":
        raise HTTPException(status_code=401, detail="Only Admin can create products")

    try:
        image_url = await upload_image(product.image)

        if not image_url:
            raise HTTPException(status_code=404, detail="Image Not Found")

        new_product = await prisma.product.create(
            data={
                "name": product.name,
                "description": product.description,
                "price": float(product.price),
                "quantity": product.quantity,
                "category": product.category,
                "imageUrl": image_url,
                "availableQuantity":product.quantity
            }
        )

        return new_product
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/",response_model=List[ProductOut])
async def list_products():
    return  await prisma.product.find_many(
        order={
            "createdAt":'desc'
        }
    )

@router.get("/{product_id}",response_model=ProductOut)
async def get_product(product_id:str):
    product = await prisma.product.find_unique(
        where={
            "id":product_id,
        }
    )
    if not product:
        raise HTTPException(status_code=404,detail="Product Not Found")

    return product


@router.put("/{product_id}",response_model=ProductOut)
async def update_product(product_id:str,product:ProductOut,current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=400, detail="User Does not exist")

    if current_user.role != "ADMIN":
        raise HTTPException(status_code=401, detail="Only Admin can update products")

    updated_product = prisma.product.update(
        where={
            "id":product_id,
        },
        data=product.model_dump(exclude_unset=True)
    )
    return updated_product


@router.delete("/{product_id}",response_model=ProductOut)
async def delete_product(product_id:str,current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=400, detail="User Does not exist")
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=401, detail="Only Admin can delete products")

    delete_product = prisma.product.delete(
        where={
            "id":product_id,
        }
    )

    return delete_product

