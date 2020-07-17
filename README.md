# flight

### An app that tells you in real time what flight with the lowest opportunity cost will be within the next 24 hours

## TO DO

1. Create functionality

  - Create list of airports flight code
    * This will be a list of flight objects
    * A flight object contains several attributes
      - flight number as airline code and number(e.g. UA7013)
      - Source airport
      - Destination airport
      - Distance as the crow flies
      - Price
      - Opportunity Cost -- calculated from price and distance
  - Use travelpayouts' cheapest flights API to narrow down the amount of flights that I have to sort through
    * This being because I'm going to want a flight with a low price regardless.
    * The price will be in USD 
  - Find the flight with the lowest opportunity cost

2. Make it deployable

  - A Twitter bot
  - posts every day at 7:30am PST as to what the cheapest flight in the next 24 hours will be
  - provides a link to buy the ticket
  - Eventually I would like to make this a website that operates in real-time, but for now, baby steps
