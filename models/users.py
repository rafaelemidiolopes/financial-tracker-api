from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    transactions: Mapped[list['Transaction']] = relationship('Transaction', back_populates='user')
    password_hash: Mapped[str] = mapped_column(String(300))
    is_active: Mapped[bool] = mapped_column(default=True)