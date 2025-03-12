from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Date
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

class Sale(Base):
    __tablename__ = "sales"

    sale_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    region: Mapped[str] = mapped_column(String(50), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    sale_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    etf_symbol: Mapped[str] = mapped_column(String, nullable=False)

class Customer(Base):
    __tablename__ = "customers"

    customer_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    signup_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    country: Mapped[str] = mapped_column(String(50), nullable=False)

class CustomerTransaction(Base):
    __tablename__ = "customer_transactions"

    transaction_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.customer_id"), nullable=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    transaction_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    etf_symbol: Mapped[str] = mapped_column(String(10), nullable=False)


if __name__ == '__main__':
    Base.metadata.create_all(engine)