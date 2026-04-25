from fastapi import APIRouter, Depends
from schemas.transactions import TransactionCreate, TransactionResponse, TransactionUpdate
from database import get_db
from sqlalchemy.orm import Session
from services import transactions
from core.security import get_current_user
from models.users import User

router = APIRouter()

@router.post('/transaction', response_model=TransactionResponse)
def create_transaction(data: TransactionCreate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    return transactions.create_transaction(current_user, data, db)

@router.get('/transaction', response_model=list[TransactionResponse])
def get_transactions(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return transactions.get_transactions(current_user, db)

@router.patch('/transaction/{transaction_id}', response_model=TransactionResponse)
def update_transaction(transaction_id: int, new_data: TransactionUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return transactions.update_transaction(transaction_id, new_data, db)

@router.delete('/transaction/{transaction_id}', status_code=204)
def delete_transaction(transaction_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return transactions.delete_transaction(transaction_id, db)