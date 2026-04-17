from pydantic import BaseModel, ConfigDict
from models.transactions import Type

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