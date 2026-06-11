from fastapi import FastAPI, Request
from routers.users import router as users_router
from routers.transactions import router as transaction_router
from models.users import User 
from models.transactions import Transaction
from database import Base, engine
from contextlib import asynccontextmanager
import logger_config
import uuid
from prometheus_client import Counter, Histogram
import time

REQUEST_COUNT = Counter('total_requests', 'number of total requests', ['method', 'endpoint', 'status'])

REQUEST_DURATION = Histogram('requests_duration', 'requests time duration', ['method', 'endpoint'])

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
        
        start_endpoint_time = time.time()
    
        response = await call_next(request)
        
        request_duration = time.time() - start_endpoint_time
        
        response.headers["X-Request-ID"] = request_id
        
        logger_config.logger.info(f'Request finished. Request method: {request.method}. Request url: {request.url.path}. Status code: {response.status_code}')
    
    REQUEST_DURATION.labels(method = request.method, endpoint = request.url.path).observe(request_duration)
    
    REQUEST_COUNT.labels(method = request.method, endpoint = request.url.path, status = str(response.status_code)).inc()
    
    return response

app.include_router(transaction_router)
app.include_router(users_router)