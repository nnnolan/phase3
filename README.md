# Airline Reservation System

## Setup

1. Get MySQL running! (macbook)
```
brew install mysql
brew services start mysql 
```

2. Create the database and load the SQL files:
```
mysql -u root -e "CREATE DATABASE airline_db;"
mysql -u root airline_db < airline.sql
mysql -u root airline_db < seed.sql
```

3. Install the Python dependency:
```
pip install mysql-connector-python
```

(dropping db)
```
mysql -u root -e "DROP DATABASE IF EXISTS airline_db;"
```

## Running it

Just call whichever function you want, using command

```
python app.py (command)
```

The three functions (and an example call) are:
- `python airplane.py search_available_flights("JFK", "LAX", "2026-05-01")`
- `python airplane.py make_reservation_and_book_ticket("P001", "FL-101", "Credit Card")`
- `python airplane.py view_itinerary("RES-001")`


