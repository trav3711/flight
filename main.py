#IMPORTS
import pandas as pd
from datetime import datetime, timedelta
import requests
import json
import tools
import sys

#API REQUEST
#response = requests.get(f'http://api.travelpayouts.com/v1/prices/cheap?origin=SFO&depart_date=2020-07-30&currency=USD&token=2ceebb2ac13021c42173c017f48805e1')
#json_data = json.loads(response.text)
#print(json.dumps(json_data, indent=4, sort_keys=True))

#GET DATA
airports = pd.read_csv('./data/airports.csv')
routes = pd.read_csv('./data/routes.csv')

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

        self.distance = tools.dist_func(lt1, lg1, lt2, lg2)

    def set_cost(self):
        self.cost = self.price/self.distance
        print(self.cost)

    def __str__(self):
        return f'this is flight {self.airline}{self.flight_number} from {self.source} to {self.dest} and it costs ${self.price}'

class Airport():
    iata_code = ''

    def __init__(self, name, code, id, longitude, latitude):
         self.name = name
         self.iata_code = code
         self.id = id
         self.longitude = longitude
         self.latitude = latitude

    def __str__(self):
        return f'name: {self.name}, code: {self.iata_code}, id: {self.id}'

#CREATE A LIST OF LARGE AIRPORTS AROUND THE WORLD
def create_airport_list():
    large_airport_list = []
    types = airports['type']

    for i in range(len(types)):

        if  types[i] == 'large_airport':

            name = str(airports.loc[i, 'name'])
            id = int(airports.loc[i, 'id'])
            code = str(airports.loc[i, 'iata_code'])
            long = float(airports.loc[i, 'longitude_deg'])
            lat = float(airports.loc[i, 'latitude_deg'])

            large_airport_list.append(Airport(name, code, id, long, lat))

    airport_list = sorted(large_airport_list, key=lambda code: Airport.iata_code)
    return large_airport_list

#CREATES LIST OF JSON DATA RELATIVE TO AIRPORT LIST A LIST OF FLIGHTS
def create_flight_list():
    airport_list = create_airport_list()
    flight_list = []
    year, month, day = get_now()
    print('built airport list')

    for Airport in airport_list:

        response = requests.get(f'http://api.travelpayouts.com/v1/prices/cheap?origin={Airport.iata_code}&depart_date={year}-{month}-{day}&currency=USD&token=2ceebb2ac13021c42173c017f48805e1')
        json_data = json.loads(response.text)

        if (json_data["data"] != {}):
            #print(f'\nDEPARTING FROM {airport}:\n')
            #print(json.dumps(json_data, indent=4, sort_keys=True))

            try:
                for dest in json_data["data"]:
                    Destination = find_airport(dest, airport_list)

                    for num in json_data["data"][dest]:
                        price = json_data["data"][dest][num]['price']
                        airline = json_data["data"][dest][num]['airline']
                        flight_number = json_data["data"][dest][num]['flight_number']
                        new_flight = Flight(Airport, Destination, airline, flight_number, price)
                        flight_list.append(new_flight)
            except:
                print('SKIPPED')
                pass

    return flight_list

def find_airport(dest, arr):
    for Airport in arr:
        if Airport.iata_code == dest:
            print(Airport)
            return Airport

def find_best_flight(flights):
    best = flights[0]
    for flight in flights:
        #print(flight.cost)
        if flight.cost < best.cost:
            best = flight
    return best

#returns current month and year
def get_now():
    now = datetime.now() + timedelta(days=2)
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    return year, month, day


def main():

    #airports = create_airport_list()
    #new_source = airports.pop()
    #new_dest = airports.pop()
    #print(f"name: {new_source.name} x1: {new_source.latitude} y1: {new_source.longitude}")
    #print(f'name: {new_dest.name} x2: {new_dest.latitude} y2: {new_dest.longitude}')
    #flight = Flight(new_source, new_dest, 'NK', 2869, 216)

    #flight.set_distance()
    #flight.set_cost()

    #print(flight.distance)
    #print(flight.price)
    #print(flight.cost)


    flights = create_flight_list()
    print("built flight list")

    for flight in flights:
        try:
            flight.set_distance()
            flight.set_cost()
        except:
            pass


    best_flight = find_best_flight(flights)
    print(best_flight)

if __name__ == "__main__":
    main()
