from typing import List, Optional
from pydantic import BaseModel

class AirportBase(BaseModel):
    iata_code: str

class AirportCreate(AirportBase):
    name: str
    longitude: float
    latitude: float

class Airport(AirportBase):
    id: int
    name: str
    longitude: float
    latitude: float

    class Config:
        orm_mode = True

class FlightBase(BaseModel):
    flight_number: str

class FlightCreate(FlightBase):
    airline: str
    price: float
    distance: int
    src: str
    dest: str

class Flight(FlightBase):
    airline: str
    price: float
    distance: int
    cost: int
    src: str
    dest: str

    class Config:
        orm_mode = True
