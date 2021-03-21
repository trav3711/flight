from typing import List
import pandas as pd

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas, logic
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/init")
def init_airports(db: Session=Depends(get_db)):
    airports = logic.create_airport_list()
    for airport in airports.values():
        db_airport = crud.get_airport(db, code=airport.iata_code)
        if db_airport:
            continue
        else:
            crud.create_airport_from_model(
                db,
                airport.iata_code,
                airport.name,
                airport.longitude,
                airport.latitude
            )

@app.get("/")
def hello_world():
    return {"message": "hello world"}

@app.get("/airports", response_model = schemas.Airport)
def get_airports(airport: schemas.AirportBase, db: Session=Depends(get_db)):
    db_airport = crud.get_airport(db=db, code=airport.iata_code)
    if not db_airport:
        raise HTTPException(status_code=404, detail="Airport not found")
    return db_airport

@app.post("/airports")
def create_airport(airport: schemas.AirportCreate, db: Session=Depends(get_db)):
    db_airport = crud.get_airport(db, code=airport.iata_code)
    if db_airport:
        raise HTTPException(status_code=400, detail="Airport already registered")
    return crud.create_airport(db=db, airport=airport)
