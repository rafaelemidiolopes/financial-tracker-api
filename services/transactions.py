from sqlalchemy.orm import Session
from schemas.transactions import TransactionCreate, TransactionUpdate, TransactionFilters
from models.transactions import Transaction
from models.users import User
from fastapi import HTTPException
from models.transactions import Type

def create_transaction(current_user, data: TransactionCreate, db: Session):
    new_transaction = Transaction(user_id= current_user.id, type = data.type, amount = data.amount, category = data.category, description = data.description)
    
    db.add(new_transaction)
    
    db.commit()
    
    db.refresh(new_transaction)
    
    return new_transaction

def get_transactions(filters: TransactionFilters, current_user: User, db: Session):
    query = db.query(Transaction).filter_by(user_id = current_user.id)
    
    if filters.type:
        if not Type(filters.type):       
            raise HTTPException(status_code=422,
                detail=f"Invalid type: '{filters.type}'. Must be 'income' or 'expense'.")
            
        query = query(Transaction).filter_by(type = filters.type)
    
    if filters.min_amount:
        query = query(Transaction).filter(Transaction.amount >= filters.min_amount)
    
    if filters.max_amount:
        query = query(Transaction).filter(Transaction.amount <= filters.max_amount)
    
    if filters.category:
        query = query(Transaction).filter_by(category = filters.category)
    
    return query.all()

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