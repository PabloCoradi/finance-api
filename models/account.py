from db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    interest  = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="accounts")
    expenses = relationship("Expense", back_populates="account")
    final_balances = relationship("FinalBalance", back_populates="account")