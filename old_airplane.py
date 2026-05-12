import mysql.connector
import random
import string
from datetime import date
import sys

# database 
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="", # no password
    database="airline_db"
)
cursor = conn.cursor(dictionary=True)


# handy function to generate unique IDs for reservations, payments, and tickets
def generate_id(prefix):
    return prefix + "-" + ''.join(random.choices(string.digits, k=6))


# serach for flighjts based on departure, arrival, and date
def search_available_flights(departure_loc, arrival_loc, travel_date):
    cursor.execute("""
        SELECT f.flight_ID, f.departure, f.arrival, f.status,
               ac.make, ac.model
        FROM Flight f
        JOIN Aircraft ac ON f.serial_num = ac.serial_num
        WHERE f.departure_loc = %s AND f.arrival_loc = %s AND DATE(f.departure) = %s
    """, (departure_loc, arrival_loc, travel_date))

    flights = cursor.fetchall()

    if not flights:
        print("No flights found.")
        return

    # for each flight, also get total seats and taken seats to show availability
    for f in flights:
        cursor.execute("SELECT COUNT(*) AS total FROM Seat WHERE flight_ID = %s", (f["flight_ID"],))
        total = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS taken FROM Ticket_Seat WHERE flight_ID = %s", (f["flight_ID"],))
        taken = cursor.fetchone()["taken"]

        print(f"Flight: {f['flight_ID']} | {f['departure']} -> {f['arrival']} | {f['make']} {f['model']} | Status: {f['status']} | Seats available: {total - taken}")


# make reservation, book ticket, and assign seat
def make_reservation_and_book_ticket(passport_id, flight_id, method):
    # get or create passenger
    cursor.execute("SELECT * FROM Passenger WHERE passport_id = %s", (passport_id,))
    passenger = cursor.fetchone()

    if not passenger:
        print("Passenger not found. Quitting...")
        raise Exception("Passenger not found. Please register first.")
    
    # check available seats
    cursor.execute("SELECT * FROM Seat WHERE flight_ID = %s", (flight_id,))
    all_seats = cursor.fetchall()

    # get taken seats for this flight
    cursor.execute("SELECT seating_no, seating_row FROM Ticket_Seat WHERE flight_ID = %s", (flight_id,))
    taken = {(r["seating_no"], r["seating_row"]) for r in cursor.fetchall()}
    available = [s for s in all_seats if (s["seating_no"], s["seating_row"]) not in taken]

    if not available:
        print("No seats available on this flight.")
        return

    # just get a seat, not that big of a deal for ad emo
    seat = random.choice(available)
    price = {"First": 1200.00, "Business": 750.00, "Economy": 300.00}.get(seat["class"], 300.00)

    # create payment
    payment_id = generate_id("PAY")
    cursor.execute("INSERT INTO Payment (payment_id, amount, method) VALUES (%s,%s,%s)", (payment_id, price, method))

    # create reservation
    reservation_id = generate_id("RES")
    cursor.execute(
        "INSERT INTO Reservation (reservation_id, booking_date, status, passport_id, payment_id) VALUES (%s,%s,'Confirmed',%s,%s)",
        (reservation_id, date.today(), passport_id, payment_id)
    )

    # link to flight
    cursor.execute("INSERT INTO Reservation_Flight (reservation_id, flight_ID) VALUES (%s,%s)", (reservation_id, flight_id))

    # create ticket
    ticket_id = generate_id("TKT")
    cursor.execute("INSERT INTO Ticket (ticket_id, issue_date, price, reservation_id) VALUES (%s,%s,%s,%s)", (ticket_id, date.today(), price, reservation_id))

    # assign seat
    cursor.execute("INSERT INTO Ticket_Seat (ticket_id, seating_no, seating_row, flight_ID) VALUES (%s,%s,%s,%s)", (ticket_id, seat["seating_no"], seat["seating_row"], flight_id))

    conn.commit()

    print(f"Booking confirmed! Reservation: {reservation_id} | Ticket: {ticket_id} | Seat: {seat['seating_row']}{seat['seating_no']} ({seat['class']}) | Price: ${price:.2f} | Payment: {payment_id}")


#view itenary for a reservation, showing passenger details, 
#  flight info, seat assignment, and payment status
def view_itinerary(reservation_id):
    cursor.execute("SELECT * FROM Reservation WHERE reservation_id = %s", (reservation_id,))
    res = cursor.fetchone()
    if not res:
        print("Reservation not found.")
        return

    # get passenger info
    cursor.execute("SELECT * FROM Passenger WHERE passport_id = %s", (res["passport_id"],))
    p = cursor.fetchone()

    # get payment info
    cursor.execute("SELECT * FROM Payment WHERE payment_id = %s", (res["payment_id"],))
    pay = cursor.fetchone()

    # now we get flight info
    # namely, a flight can have multiple legs, so we join through 
    # the Reservation_Flight table to get all flights for this reservation
    cursor.execute("""
        SELECT f.flight_ID, f.departure, f.arrival, f.departure_loc, f.arrival_loc, f.status, ac.make, ac.model
        FROM Reservation_Flight rf
        JOIN Flight f ON rf.flight_ID = f.flight_ID
        JOIN Aircraft ac ON f.serial_num = ac.serial_num
        WHERE rf.reservation_id = %s
    """, (reservation_id,))
    flights = cursor.fetchall()

    # tickt info
    cursor.execute("SELECT * FROM Ticket WHERE reservation_id = %s", (reservation_id,))
    tickets = cursor.fetchall()

    # print everything related to the passenger
    print(f"\nPassenger: {p['first_name']} {p['last_name']} | Email: {p['email']}")
    print(f"Reservation: {res['reservation_id']} | Status: {res['status']} | Booked: {res['booking_date']}")
    print(f"Payment: ${pay['amount']} via {pay['method']} ({pay['payment_id']})")

    # flight info
    for f in flights:
        print(f"Flight: {f['flight_ID']} | {f['departure_loc']} -> {f['arrival_loc']} | {f['departure']} -> {f['arrival']} | {f['make']} {f['model']} | {f['status']}")

    # for each ticket, also get seat assignemnt
    for t in tickets:
        cursor.execute("""
            SELECT ts.seating_no, ts.seating_row, s.class
            FROM Ticket_Seat ts
            JOIN Seat s ON ts.seating_no = s.seating_no AND ts.seating_row = s.seating_row AND ts.flight_ID = s.flight_ID
            WHERE ts.ticket_id = %s
        """, (t["ticket_id"],))
        seat = cursor.fetchone()
        print(f"Ticket: {t['ticket_id']} | ${t['price']:.2f} | Seat: {seat['seating_row']}{seat['seating_no']} ({seat['class']})")



if len(sys.argv) < 2:
    print("Usage:")
    print("  python app.py search <departure> <arrival> <date>")
    print("  python app.py book <passport_id> <flight_id> <method>")
    print("  python app.py itinerary <reservation_id>")
else:
    cmd = sys.argv[1]
    if cmd == "search":
        search_available_flights(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == "book":
        make_reservation_and_book_ticket(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == "itinerary":
        view_itinerary(sys.argv[2])
    else:
        print(f"Unknown command: {cmd}")
        

### example calls
# python airplane.py search "JFK" "LAX" "2026-05-01"
# python airplane.py book "P001" "FL-101" "Credit Card"
# python airplane.py itinerary "RES-001"
