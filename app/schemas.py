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
    airline: str
    price: float
    distance: int

class FlightCreate(FlightBase):
    cost: int

class Flight(FlightBase):
    flight_number: str

    class Config:
        orm_mode = True
