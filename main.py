from fastapi import FastAPI
from src.db import prisma
from src.apis import auth
app = FastAPI()

@app.on_event("startup")
async def startup():
    await prisma.connect()


@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()




@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(auth.router,prefix="/api/auth",tags=["Authentication"])
