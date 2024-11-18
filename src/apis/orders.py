
from src.db import prisma
from fastapi import APIRouter, Depends, HTTPException

from src.models.schema import CreateOrderRequest, PaymentResponse
from src.utils.auth import get_current_user
from src.utils.mpesa_config import initiate_stk_push

router = APIRouter()

@router.post("/", response_model=CreateOrderRequest)
async def create_order(order: CreateOrderRequest,current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=404,detail="User does not exist")

    product = prisma.product.find_unique(
        where={
            "id": order.productId,
        }
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product does not exist")

    payment_success = await initiate_stk_push(float(order.totalPrice), current_user.phone, order.productId)

    if not payment_success:
        return PaymentResponse(success=False, message="Payment failed")



    new_order = prisma.order.create(
        data={
            "userId":current_user.id,
            "addressId":order.addressId,
            "status": "PAID",
            "totalAmount":float(order.totalPrice),
            "items":{
                "create":[
                    {
                        "productId": order.productId,
                        "quantity": order.quantity,
                        "price": product.price,
                    }
                ]
            }

        },
    include = {"items": True},
    )

    if new_order:
         prisma.product.update(
            where={
                "id":product.id
            },
            data={
                "availableQuantity":product.availableQuantity - order.quantity
            }
        )

    return PaymentResponse(success=True, message="Order created successfully", order_id=order.id)
    