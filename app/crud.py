from sqlalchemy.orm import Session

from . import models, schemas

def get_airport(db: Session, code: str):
    return db.query(models.Airport).filter(models.Airport.iata_code == code).first()

def create_airport(db: Session, airport: schemas.AirportCreate):
    new_airport = models.Airport(
        name = airport.name,
        iata_code = airport.iata_code,
        longitude = airport.longitude,
        latitude = airport.latitude
    )
    db.add(new_airport)
    db.commit()
    db.refresh(new_airport)
    return new_airport

def create_airport_from_model(db: Session, code: str, name: str, longitude: float, latitude: float):
    new_airport = models.Airport(
        name = name,
        iata_code = code,
        longitude = longitude,
        latitude = latitude
    )
    db.add(new_airport)
    db.commit()
    db.refresh(new_airport)
    return new_airport

def get_flight(db: Session, flight_number: str):
    return db.query(models.Flight).filter(models.Flight.flight_number == flight_number).first()

def get_flights_from_src(db: Session, src_code: str, limit: int = 10):
    return db.query(models.Flight).filter(models.Flight.source.iata_code == src_code).limit(limit).all()

def create_flight():
    pass

def update_flight():
    pass
