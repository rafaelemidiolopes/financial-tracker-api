from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Base
from models.transactions import Transaction
from models.users import User

DATABASE_URL_FAKE = "sqlite:///./test_database.db"

test_engine = create_engine(DATABASE_URL_FAKE)

TestingSessionLocal = sessionmaker(autocommit = False, autoflush= False, bind = test_engine)

Base.metadata.create_all(bind = test_engine)

def override_get_db(): 
    fake_db = TestingSessionLocal()
    
    try:
        yield fake_db
        
    finally:
        fake_db.close()