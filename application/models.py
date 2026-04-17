from typing import List

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import  Column, DateTime, Float, ForeignKey, String



class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

service_mechanics = db.Table(
    "service_mechanics",
    Base.metadata,
    Column("service_ticket_id",ForeignKey("service_tickets.id"), primary_key=True),
    Column("mechanic_id",ForeignKey("mechanics.id"), primary_key=True)
)


class Costumer(Base):
    __tablename__ = "costumers"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    phone: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(200), unique=True)
    password: Mapped[str] = mapped_column(String(50), nullable=False)

    service_tickets: Mapped[List["ServiceTicket"]] = relationship(back_populates="costumer", cascade="all, delete-orphan") # This sets up a one-to-many relationship between Costumer and ServiceTicket. The cascade option ensures that when a Costumer is deleted, all associated ServiceTickets are also deleted.

class ServiceTicket(Base):
    __tablename__ = "service_tickets"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    VIN: Mapped[str] = mapped_column(String(50), nullable=False)
    service_date: Mapped[DateTime] = mapped_column(DateTime)
    service_desc: Mapped[str] = mapped_column(String(200))

    costumer_id: Mapped[int] = mapped_column(ForeignKey("costumers.id"), nullable=False)# ForeignKey to link to costumer one to many relationship
    costumer: Mapped[Costumer] = relationship(back_populates="service_tickets")
    mechanics: Mapped[List["Mechanic"]] = relationship(secondary=service_mechanics, back_populates="service_tickets")

class Mechanic(Base):
    __tablename__ = "mechanics"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True)
    phone: Mapped[str] = mapped_column(String(200))
    salary: Mapped[float] = mapped_column(Float)

    service_tickets: Mapped[List[ServiceTicket]] = relationship(secondary=service_mechanics, back_populates="mechanics")



