from fastapi import FastAPI, Request
from routers.users import router as users_router
from routers.transactions import router as transaction_router
from models.users import User 
from models.transactions import Transaction
from database import Base, engine
from contextlib import asynccontextmanager
import logger_config
import uuid

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    
    yield
    
app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def add_request_id(request: Request, call_next):

    request.state.request_id = str(uuid.uuid4())

    response = await call_next(request)

    return response

app.include_router(transaction_router)
app.include_router(users_router)