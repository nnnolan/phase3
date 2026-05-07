-- Airline Reservation System Database Schema
-- compared to my diagram in phase two, i added not null to any columns where there shouldnt be a null
-- https://stackoverflow.com/a/1583701

CREATE TABLE IF NOT EXISTS Airport (
    IATA_code VARCHAR(10) PRIMARY KEY,
    city VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    timezone VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Aircraft (
    serial_num VARCHAR(20) PRIMARY KEY,
    make VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Passenger (
    passport_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    miles INT NOT NULL
);

CREATE TABLE IF NOT EXISTS Payment (
    payment_id VARCHAR(20) PRIMARY KEY,
    amount DECIMAL(20, 2) NOT NULL,
    method VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS Reservation (
    reservation_id VARCHAR(20) PRIMARY KEY,
    booking_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL,
    passport_id VARCHAR(20) NOT NULL,
    payment_id VARCHAR(20) NOT NULL UNIQUE,
    FOREIGN KEY (passport_id) REFERENCES Passenger(passport_id),
    FOREIGN KEY (payment_id) REFERENCES Payment(payment_id)
);

CREATE TABLE IF NOT EXISTS Flight (
    flight_ID VARCHAR(20) PRIMARY KEY,
    FAA_call_sign VARCHAR(20) NOT NULL,
    departure DATETIME NOT NULL,
    arrival DATETIME NOT NULL,
    departure_loc VARCHAR(100) NOT NULL,
    arrival_loc VARCHAR(100) NOT NULL,
    times INT NOT NULL,
    status VARCHAR(20) NOT NULL,
    serial_num VARCHAR(20) NOT NULL,
    FOREIGN KEY (departure_loc) REFERENCES Airport(IATA_code),
    FOREIGN KEY (arrival_loc) REFERENCES Airport(IATA_code),
    FOREIGN KEY (serial_num) REFERENCES Aircraft(serial_num)
);

CREATE TABLE IF NOT EXISTS Ticket (
    ticket_id VARCHAR(20) PRIMARY KEY,
    issue_date DATE NOT NULL,
    price DECIMAL(20, 2) NOT NULL,
    reservation_id VARCHAR(20) NOT NULL,
    FOREIGN KEY (reservation_id) REFERENCES Reservation(reservation_id)
);

CREATE TABLE IF NOT EXISTS Seat (
    seating_no VARCHAR(10) NOT NULL,
    seating_row VARCHAR(10) NOT NULL,
    flight_ID VARCHAR(20) NOT NULL,
    class VARCHAR(20) NOT NULL,
    boarding_prio INT NOT NULL,
    PRIMARY KEY (seating_no, seating_row, flight_ID),
    FOREIGN KEY (flight_ID) REFERENCES Flight(flight_ID)
);

-- junction table: reservation <-> flight (M:N)
CREATE TABLE IF NOT EXISTS Reservation_Flight (
    reservation_id VARCHAR(20) NOT NULL,
    flight_ID VARCHAR(20) NOT NULL,
    PRIMARY KEY (reservation_id, flight_ID),
    FOREIGN KEY (reservation_id) REFERENCES Reservation(reservation_id),
    FOREIGN KEY (flight_ID) REFERENCES Flight(flight_ID)
);

-- junction table: ticket <-> seat (1:1)
CREATE TABLE IF NOT EXISTS Ticket_Seat (
    ticket_id VARCHAR(20) PRIMARY KEY,
    seating_no VARCHAR(10) NOT NULL,
    seating_row VARCHAR(10) NOT NULL,
    flight_ID VARCHAR(20) NOT NULL,
    FOREIGN KEY (ticket_id) REFERENCES Ticket(ticket_id),
    FOREIGN KEY (seating_no, seating_row, flight_ID) REFERENCES Seat(seating_no, seating_row, flight_ID),
    UNIQUE (seating_no, seating_row, flight_ID)
);