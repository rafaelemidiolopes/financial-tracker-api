from sqlalchemy.orm import Session
from schemas.transactions import TransactionCreate, TransactionUpdate, TransactionFilters
from models.transactions import Transaction
from models.users import User
from fastapi import HTTPException
from models.transactions import Type
from loguru import logger

def create_transaction(current_user, data: TransactionCreate, db: Session):
    new_transaction = Transaction(user_id= current_user.id, type = data.type, amount = data.amount, category = data.category, description = data.description)
    try:
        db.add(new_transaction)
        
        db.commit()
    
        db.refresh(new_transaction)
        
        logger.info(f'Transaction created. Id transaction: {new_transaction.id}. User id: {new_transaction.user_id}')
    
    except Exception:
        db.rollback()
        
        logger.exception(f'Error creating transaction. User: {current_user.id}.')
        
        raise
    
    return new_transaction

def get_transactions(filters: TransactionFilters, current_user: User, db: Session):
    try:
        query = db.query(Transaction).filter_by(user_id=current_user.id)
        
        if filters.type:
            query = query.filter_by(type=filters.type)
        
        if filters.min_amount is not None:
            query = query.filter(Transaction.amount >= filters.min_amount)
        
        if filters.max_amount is not None:
            query = query.filter(Transaction.amount <= filters.max_amount)
        
        if filters.category:
            query = query.filter_by(category=filters.category)
            
        if filters.start_date:
            query = query.filter(Transaction.created_at >= filters.start_date)
        
        if filters.end_date:
            query = query.filter(Transaction.created_at <= filters.end_date)
        
        transactions = query.all()
        
        logger.info(f'{len(transactions)} transactions fetched for user {current_user.id}')
        
        return transactions
    
    except Exception:
        logger.exception(f'Error when viewing transactions! User: {current_user.id}')
        
        raise

def update_transaction(transaction_id: int, new_data: TransactionUpdate, current_user: User, db: Session):
    transaction = db.query(Transaction).filter_by(id = transaction_id, user_id = current_user.id).first()
    
    if not transaction:
        logger.warning(f'Transaction {transaction_id} not found for user {current_user.id}')
        
        raise HTTPException(status_code=404, detail='Transaction not found! ')
    
    dict_new_data = new_data.model_dump(exclude_unset=True)
    
    for field, value in dict_new_data.items():
        setattr(transaction, field, value)
    
    try:     
        db.commit()
        
        db.refresh(transaction)
        
        logger.info(f'Transaction {transaction.id} updated by user {current_user.id}!')
        
    except Exception:
        db.rollback()
        
        logger.exception(f'Error when updating transaction. User: {current_user.id}')
        
        raise
    
    return transaction

def delete_transaction(transaction_id: int, current_user: User, db: Session):
    transaction = db.query(Transaction).filter_by(id = transaction_id, user_id = current_user.id).first()
    
    if not transaction:
        logger.warning(f'Transaction {transaction_id} not found for user {current_user.id}')
        
        raise HTTPException(status_code=404, detail='Transaction not found! ')
    
    try: 
        db.delete(transaction)
        
        db.commit()
        
    except Exception:
        db.rollback()
        
        logger.exception(f'Error when delete transaction {transaction.id}. User: {current_user.id}')
        
        raise
    
    logger.info(f'Transaction {transaction.id} deleted by {current_user.id}! ')