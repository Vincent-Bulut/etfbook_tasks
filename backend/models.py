from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey
from datetime import datetime

from backend.database import engine

Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    etf_symbol: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    transaction_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    parent_transaction_id: Mapped[int | None] = mapped_column(ForeignKey("transactions.transaction_id"), nullable=True)

if __name__ == '__main__':
    Base.metadata.create_all(engine)