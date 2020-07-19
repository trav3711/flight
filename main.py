#IMPORTS
import pandas as pd
from datetime import datetime, timedelta
import requests
import json
from tools import binarySearch

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
        self.distance = 0
        self.cost = 0

    def get_distance(self):
        #print(len(airports['iata_code']))
        origin_index = binarySearch(airports['iata_code'], 0, len(airports['iata_code'])-1, self.source)
        print(origin_index)
        #print('here')
        dest_index = binarySearch(airports['iata_code'], 0, len(airports['iata_code'])-1, self.dest)

        source_latitude = airports.loc[origin_index, 'latitude_deg']
        source_longitude = airports.loc[origin_index, 'longitude_deg']
        dest_latitude = airports.loc[self.dest, 'latitude_deg']
        dest_longitude = airports.loc[self.dest, 'longitude_deg']
        return dist_func(source_longitude, source_latitude, dest_longitude, dest_latitude)

    def dist_func(long1, lat1, long2, lat2):
        return 0

    def cost():
        return 0

    def __str__(self):
        return f'this flight is from {self.source} to {self.dest} on {self.airline}'


#CREATE A LIST OF LARGE AIRPORTS AROUND THE WORLD
def create_airport_list():
    large_airport_list = []
    types = airports['type']

    for i in range(len(types)):

        if  types[i] == 'large_airport':
            #print(type(airports.loc[i, 'iata_code']))
            large_airport_list.append(str(airports.loc[i, 'iata_code']))

    return large_airport_list

#CREATES LIST OF JSON DATA RELATIVE TO AIRPORT LIST A LIST OF FLIGHTS
def create_flight_list():
    airport_list = create_airport_list()
    airport_list.sort()
    flight_list = []
    year, month, day = get_now()
    #print('here')

    for airport in airport_list:
        print(airport)
        response = requests.get(f'http://api.travelpayouts.com/v1/prices/cheap?origin={airport}&depart_date={year}-{month}-{day}&currency=USD&token=2ceebb2ac13021c42173c017f48805e1')
        #print(response)
        json_data = json.loads(response.text)

        if (json_data["data"] != {}):
            #print(f'\nDEPARTING FROM {airport}:\n')
            #print(json.dumps(json_data, indent=4, sort_keys=True))

            try:
                for dest in json_data["data"]:
                    #print(dest)

                    for num in json_data["data"][dest]:
                        price = json_data["data"][dest][num]['price']
                        airline = json_data["data"][dest][num]['airline']
                        flight_number = json_data["data"][dest][num]['flight_number']
                        new_flight = Flight(airport, dest, airline, flight_number, price)
                        flight_list.append(new_flight)
            except:
                print('SKIPPED')
                pass

    return flight_list


#returns current month and year
def get_now():
    now = datetime.now() + timedelta(days=1)
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    return year, month, day


def main():

    flight = Flight('AFW', 'ATL', 'NK', 2869, 216)
    flight.get_distance()


    #flights = create_flight_list()
    #print(len(flights))
    #print("DONE")
    #for flight in flights:
    #    flight.get_distance()
    #    flight.cost()

    #print(airports['iata_code'])
    #print(airports.loc[0])
    #print(routes.loc[1, ' source airport'])

    #flights = create_flight_list()
    #flights[0].get_distance()
    #print(available_routes)

    #print(response.content)
    pass

if __name__ == "__main__":
    main()
