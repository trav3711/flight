from typing import List
import pandas as pd
import requests, json
from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi_utils.tasks import repeat_every
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import crud, models, schemas, logic
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/dashboard", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

def get_now():
    now = datetime.now() + timedelta(days=7)
    year = now.strftime("%Y")
    month = now.strftime("%m")
    #day = now.strftime("%d")
    return year, month

def make_request(src: str = None):
    year, month = get_now()
    #print(str(year), str(month), str(day))
    url = "https://api.travelpayouts.com/v2/prices/latest"
    querystring = {
        "currency":"usd",
        "show_to_affiliates":"true",
        "origin": src,
        "one_way": "true",
        "beginning_of_period": "{}-{}-01".format(year, month),
        "period_type": "month",
        "show_to_affiliates": "false"
    }
    headers = {'x-access-token': '2ceebb2ac13021c42173c017f48805e1'}
    response = requests.request("GET", url, headers=headers, params=querystring)
    json_data = json.loads(response.text)
    if json_data["success"] == True and json_data["data"] != {}:
        return json_data["data"]

@app.on_event("startup")
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/flights")
def update_flights_task(db: Session=Depends(get_db)) -> None:
    airports = crud.get_all_airports(db)
    for src in airports:
        flights = make_request(src.iata_code)
        try:
            for flight in flights:
                print(flight)
                if crud.get_airport(db, code=flight["destination"]):
                    crud.create_flight_from_model(
                        db,
                        depart_date = flight["depart_date"],
                        price = flight["value"],
                        distance = flight["distance"],
                        source = src.iata_code,
                        destination = flight["destination"],
                    )
        except Exception as e:
            print(e)
            break

@app.get("/init")
def init_airports(db: Session=Depends(get_db)) -> None:
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

@app.get("/", response_class = HTMLResponse)
def landing(request: Request, db: Session=Depends(get_db)):
    airports = crud.get_all_airports(db)
    return templates.TemplateResponse("home.html", {"request": request, "airports": airports})

#get top ten flights for selected airport
@app.get("/dashboard", response_class = HTMLResponse)
def read_flights(request: Request, db: Session=Depends(get_db)):
    airports = crud.get_all_airports(db)
    print(str(request.form()))
    iata_code = "POM"
    flights = crud.get_flights_from_src(db, iata_code)
    print(flights)
    params = {
        "request": request,
        "airports": airports,
        "flights": flights
    }
    return templates.TemplateResponse("dashboard.html", params)
