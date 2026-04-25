from fastapi import FastAPI
from routers.users import router as users_router
from routers.transactions import router as transaction_router
from models.users import User 
from models.transactions import Transaction
from database import Base, engine
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    
    yield
    
app = FastAPI(lifespan=lifespan)

app.include_router(transaction_router)
app.include_router(users_router)