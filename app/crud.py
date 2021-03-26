from sqlalchemy.orm import Session

from . import models, schemas

def get_all_airports(db: Session):
    return db.query(models.Airport).all()


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
    return db.query(models.Flight).filter(models.Flight.source == src_code).limit(limit).all()

def create_flight(db: Session, flight: schemas.FlightCreate):
    calculated_cost = flight.distance//flight.price

    new_flight = models.flight(
        flight_number = flight.flight_number,
        airline = flight.airline,
        price = flight.price,
        distance = flight.distance,
        cost = calculated_cost,
        source = flight.src,
        destination = flight.dest,
    )

def create_flight_from_model(db: Session, depart_date: str, price: float, distance: int, source: str, destination: str):
    calculated_cost = distance//price

    new_flight = models.Flight(
        price = price,
        distance = distance,
        cost = calculated_cost,
        source = source,
        destination = destination,
        depart_date = depart_date
    )
    db.add(new_flight)
    db.commit()
    db.refresh(new_flight)
    return new_flight

def update_flight():
    pass
