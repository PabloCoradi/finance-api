from db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, func
from sqlalchemy.orm import relationship

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    date = Column(Date, server_default=func.current_date())
    account_id = Column(Integer, ForeignKey("accounts.id"))
    account = relationship("Account", back_populates="expenses")