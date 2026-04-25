from sqlalchemy.orm import Session
from schemas.transactions import TransactionCreate, TransactionUpdate
from models.transactions import Transaction
from models.users import User
from fastapi import HTTPException

def create_transaction(current_user, data: TransactionCreate, db: Session):
    new_transaction = Transaction(user_id= current_user.id, type = data.type, amount = data.amount, category = data.category, description = data.description)
    
    db.add(new_transaction)
    
    db.commit()
    
    db.refresh(new_transaction)
    
    return new_transaction

def get_transactions(current_user, db: Session):
    return db.query(Transaction).filter_by(user_id = current_user.id).all()

def update_transaction(transaction_id: int, new_data: TransactionUpdate, db: Session):
    transaction = db.query(Transaction).filter_by(id = transaction_id).first()
    
    if not transaction:
        raise HTTPException(status_code=404, detail='Transaction not found! ')
    
    dict_new_data = new_data.model_dump(exclude_unset=True)
    
    for field, value in dict_new_data.items():
        setattr(transaction, field, value)
        
    db.commit()
    
    db.refresh(transaction)
    
    return transaction

def delete_transaction(transaction_id: int, db: Session):
    transaction = db.query(Transaction).filter_by(id = transaction_id).first()
    
    if not transaction:
        raise HTTPException(status_code=404, detail='Transaction not found! ')
    
    db.delete(transaction)
    
    db.commit()