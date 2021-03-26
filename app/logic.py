#IMPORTS
import pandas as pd
from collections import defaultdict
from datetime import datetime, timedelta
import requests
import json
import sys
import multiprocessing
from typing import Optional
from fastapi import FastAPI

def dist_func(x1, y1, x2, y2):
    r = 6378.137

    x1 = radians(x1)
    y1 = radians(y1)
    x2 = radians(x2)
    y2 = radians(y2)

    dy=y2-y1
    dist = r * acos((sin(x1)*sin(x2)) + (cos(x1)*cos(x2)*cos(dy)))
    return dist//1

class Flight:

    def __init__(self, source, dest, airline, flight_number, price):
        self.source = source
        self.dest = dest
        self.airline = airline
        self.flight_number = flight_number
        self.distance = 1
        self.price = price
        self.cost = 1


    def set_distance(self):
        lt1 = self.source.latitude
        lg1 = self.source.longitude
        lt2 = self.dest.latitude
        lg2 = self.dest.longitude

        self.distance = dist_func(lt1, lg1, lt2, lg2)

    def set_cost(self):
        self.cost = self.price/self.distance

    def __str__(self):
        return f'this is flight {self.airline}{self.flight_number} from {self.source.iata_code} to {self.dest.iata_code} and it costs ${self.price} for {self.distance} km'

class Airport():
    iata_code = ''

    def __init__(self, name=None, code=None, id=0, longitude=0, latitude=0):
         self.name = name
         self.iata_code = code
         self.id = id
         self.longitude = longitude
         self.latitude = latitude

    def __str__(self):
        return f'name: {self.name}, code: {self.iata_code}, id: {self.id}'

#CREATE A LIST OF LARGE AIRPORTS AROUND THE WORLD
def create_airport_list():
    airports = pd.read_csv('./data/airports.csv')
    large_airport_list = {}
    types = airports['type']
    #print(types)

    for i in range(len(types)):

        if  (types[i] == 'large_airport'):

            name = str(airports.loc[i, 'name'])
            id = int(airports.loc[i, 'id'])
            code = str(airports.loc[i, 'iata_code'])
            long = float(airports.loc[i, 'longitude_deg'])
            lat = float(airports.loc[i, 'latitude_deg'])

            #large_airport_list.append(Airport(name, code, id, long, lat))
            large_airport_list[code] = Airport(name, code, id, long, lat)

    airport_list = sorted(large_airport_list, key=lambda code: Airport.iata_code)
    #print(large_airport_list)
    return large_airport_list

#CREATES LIST OF JSON DATA RELATIVE TO AIRPORT LIST A LIST OF FLIGHTS
def create_flight_list():
    airport_list = create_airport_list()
    flight_list = []
    year, month, day = get_now()
    print(f'built airport list with {len(airport_list)} airports')

    for Airport in airport_list.values():
        print(Airport)

        response = requests.get(f'http://api.travelpayouts.com/v1/prices/cheap?origin={Airport.iata_code}&depart_date={year}-{month}-{day}&currency=USD&token=2ceebb2ac13021c42173c017f48805e1')
        json_data = json.loads(response.text)
        #print(json.dumps(json_data, indent=4, sort_keys=True))

        if (json_data["success"] == True) and (json_data["data"] != {}):
            #print(f'\nDEPARTING FROM {Airport}:\n')
            #print(json.dumps(json_data["data"], indent=4, sort_keys=True))

            for dest in json_data["data"]:
                try:
                    Destination = airport_list[dest]
                except KeyError:
                    #print(f'{dest} not found')
                    continue

                if Destination != 0:
                    #print(f'THE DESTINATION IS: {dest}, {Destination}')
                    for num in json_data["data"][dest]:
                        price = json_data["data"][dest][num]['price']
                        airline = json_data["data"][dest][num]['airline']
                        flight_number = json_data["data"][dest][num]['flight_number']
                        new_flight = Flight(Airport, Destination, airline, flight_number, price)
                        new_flight.set_distance()
                        flight_list.append(new_flight)
                        #print(new_flight)
                else:
                    pass
        #print('---'*20)

    return flight_list

def find_airport(dest, arr):
    for Airport in arr.values:
        if Airport.iata_code == dest:
            return Airport

    return 0

def find_best_flight(flights):
    best = flights[0]
    for flight in flights:
        #print(flight.cost)
        if (flight.cost < best.cost) and (flight.distance > 1000):
            best = flight
            print(f'The new best is, {best}')
    return best

#returns current month and year
def get_now():
    now = datetime.now() + timedelta(days=7)
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    return year, month, day


def main():

    flights = create_flight_list()
    """p1 = multiprocessing.Process(target=create_flight_list)
    p1.start()
    p1.join()
    print("built flight list")"""



    for flight in flights:
            flight.set_distance()
            #print(f'distace of {flight.distance} with price of {flight.price}')
            flight.set_cost()
            pass


    best_flight = find_best_flight(flights)
    print(best_flight)
    print(F'ORIGIN name: {best_flight.source.iata_code}, longitude: {best_flight.source.longitude}, latitude: {best_flight.source.latitude}')
    print(F'ORIGIN name: {best_flight.dest.iata_code}, longitude: {best_flight.dest.longitude}, latitude: {best_flight.dest.latitude}')
