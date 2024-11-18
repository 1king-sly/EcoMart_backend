
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
            },
            "payment": {
                "create": {
                    "amount": float(order.totalPrice),
                    "status": "COMPLETED",
                    "provider": "M-Pesa",
                    "transactionId": order.productId,
                }
            },

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


@router.get("/")
async def get_orders(current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=404,detail="User does not exist")
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403,detail="Only Admin can get orders")

    orders = prisma.order.find_many(
        order_by={
            "createdAt":"desc"
        },
        include={
            "items":True,
        }
    )

    return orders

@router.get("/me")
async def get_orders_me(current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=404,detail="User does not exist")

    orders = prisma.order.find_many(
        where={
            "userId":current_user.id,
        },
        order_by={
            "createdAt":"desc"
        },
        include={
            "items":True,
        }
    )

    return orders

@router.get("/{order_id}")
async def get_order(order_id:str, current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=404,detail="User does not exist")

    order = prisma.order.find_unique(
        where={
            "id":order_id,
        },
        include={
            "items":True,
        }
    )
    if not order:
        raise HTTPException(status_code=404,detail="Order does not exist")

    return order
