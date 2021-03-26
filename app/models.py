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

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float)
    distance = Column(Integer)
    cost = Column(Integer)
    source = Column(String, ForeignKey('airports.iata_code'))
    destination = Column(String, ForeignKey('airports.iata_code'))
    depart_date = Column(String)
