from sqlalchemy.orm import Session
from schemas.transactions import TransactionCreate
from models.transactions import Transaction

def create_transaction(current_user, data: TransactionCreate, db: Session):
    new_transaction = Transaction(user_id= current_user.id, type = data.type, amount = data.amount, category = data.category, description = data.description)
    
    db.add(new_transaction)
    
    db.commit()
    
    db.refresh(new_transaction)
    
    return new_transaction

def get_transactions(current_user, db: Session):
    return db.query(Transaction).filter_by(user_id = current_user.id).all()