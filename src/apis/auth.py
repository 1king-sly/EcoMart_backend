from datetime import timedelta
from os import access

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from prisma.models import User

from src.db import prisma
from src.models.schema import UserLogin, UserRegister, UserOut
from src.utils.auth import verify_password, ACCESS_TOKEN_EXPIRE_HOURS, create_access_token, hash_password

router = APIRouter()

@router.post('/login')
async def login(user:UserLogin):
    user_db = prisma.user.find_unique(
        where={
            "email": user.email,
        }
    )

    if not user_db:
        raise HTTPException(status_code=400, detail='User Does not exist')

    validate_password = verify_password(user.password,user_db.password)
    if not validate_password:
        raise HTTPException(status_code=401, detail='Access denied,incorrect password')



    access_token = create_access_token(
        data={"sub": user_db.email})

    return {"access_token": access_token, "token_type": "bearer"}

@router.post('/register', response_model=UserOut)
async def register(user:UserRegister):
    try:
        hashed_password = hash_password(user.password)

        new_user = prisma.user.create(
            data={
                "email": user.email,
                "name": user.name,
                "phone": user.phone,
                "password":hashed_password
            }
        )

        return new_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


