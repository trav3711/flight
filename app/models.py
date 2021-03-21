from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database import Base

class Airport(Base):
    __tablename__ = "airports"

    id = Column(Integer, primary_key=True, index=True)
    iata_code = Column(String, unique=True, index=True)
    name = Column(String)
    longitude = Column(Float)
    latitude = Column(Float)

class Flight(Base):
    __tablename__ = "flights"

    flight_number = Column(String, primary_key=True, index=True)
    airline = Column(String)
    Price = Column(Float)
    distance = Column(Integer)
    cost = Column(Integer)
