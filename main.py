#IMPORTS
import pandas as pd

#GET DATA
airports = pd.read_csv('./data/airports.csv')
routes = pd.read_csv('./data/routes.csv')

class Flight:

    def __init__(self, source, dest, airline):
        self.source = source
        self.dest = dest
        self.airline = airline

    def get_distance(self):
        source_latitude = airports.loc[self.source, 'latitude_deg']
        source_longitude = airports.loc[self.source, 'longitude_deg']
        dest_latitude = airports.loc[self.dest, 'latitude_deg']
        dest_longitude = airports.loc[self.dest, 'longitude_deg']
        return dist_func(source_longitude, source_latitude, dest_longitude, dest_latitude)

    def dist_func(long1, lat1, long2, lat2):
        pass

    def get_price():
        pass

    def cost():
        return 0

    def __str__(self):
        return f'this flight is from {self.source} to {self.dest} on {self.airline}'


#CREATE A GRAPH WITH ROUTES
#RETURNS LIST OF FLIGHT OBJECTS
def create_flight_list():
    large_airport_list = []
    flight_list = []

    types = airports['type']
    for i in range(len(types)):
        if  types[i] == 'large_airport':
            large_airport_list.append(airports.loc[i, 'iata_code'])

    for airport in large_airport_list:
        for i in range(len(routes['source airport'])):
            if routes['source airport'][i] == airport:
                #item = (airport, routes.loc[i, 'destination airport'], routes.loc[i, 'airline'])
                flight = Flight(airport, routes.loc[i, 'destination airport'], routes.loc[i, 'airline'])
                print(flight)
                flight_list.append(flight)

def main():
    #print(airports['iata_code'])
    #print(airports.loc[0])
    #print(routes.loc[1, ' source airport'])

    flights = create_flight_list()
    flights[0].get_distance()
    #print(available_routes)
    pass

if __name__ == "__main__":
    main()
