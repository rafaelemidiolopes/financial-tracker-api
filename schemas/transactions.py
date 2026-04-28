from pydantic import BaseModel, ConfigDict
from models.transactions import Type
import datetime
from fastapi import Query

class TransactionResponse(BaseModel):
    id: int
    type: Type
    amount: float
    category: str
    description: str | None = None
    
    model_config = ConfigDict(from_attributes=True)
    
class TransactionCreate(BaseModel):
    type: Type
    amount: float
    category: str
    description: str | None = None
    
class TransactionUpdate(BaseModel):
    type: Type | None = None
    amount: float | None = None
    category: str | None = None
    description: str | None = None
    
class TransactionFilters(BaseModel):
    type: Type | None = Query(None)
    amount: float | None = Query(None)
    category: str | None = Query(None)
    min_amount: float | None = Query(None)
    max_amount: float | None = Query(None)
    start_date: datetime.datetime | None = Query(None)