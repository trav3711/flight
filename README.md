# flights

### displays 10 cheapest flights fr longest distance departing from a certain airport within the next 24 hours

## TO DO

1. Manage Data(follow [this](https://fastapi.tiangolo.com/tutorial/sql-databases/))
  - create PostgreSQL DB for airports, routes and flights
    * models.py
    * database.py
    * schema.py

2. Make it deployable

  - migrate to FastAPI with HTML frontend
  - display list of 10 cheapest flights for longest distance
    * provides a link to buy the ticket
  - implement some kind fo scheduler to update flights every hour
  - environment variables
