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

    request_id = str(uuid.uuid4())
    
    request.state.request_id = request_id

    with logger_config.logger.contextualize(request_id = request_id):
        logger_config.logger.info(f'Request started. Request method: {request.method}. Request url: {request.url.path}.')
    
        response = await call_next(request)
        
        response.headers["X-Request-ID"] = request_id
        
        logger_config.logger.info(f'Request finished. Request method: {request.method}. Request url: {request.url.path}. Status code: {response.status_code}')
        
    return response

app.include_router(transaction_router)
app.include_router(users_router)