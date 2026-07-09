from db.database import Base
from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

class FinalBalance(Base):
    __tablename__ = "final_balances"

    id = Column(Integer, primary_key=True, index=True)
    balance = Column(Float, nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    account = relationship("Account", back_populates="final_balances")