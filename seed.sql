-- airports
-- code, name, country, timezone
INSERT INTO Airport VALUES ('JFK', 'New York', 'USA', 'America/New_York');
INSERT INTO Airport VALUES ('LAX', 'Los Angeles', 'USA', 'America/Los_Angeles');
INSERT INTO Airport VALUES ('LHR', 'London', 'UK', 'Europe/London');
INSERT INTO Airport VALUES ('CDG', 'Paris', 'France', 'Europe/Paris');
INSERT INTO Airport VALUES ('ORD', 'Chicago', 'USA', 'America/Chicago');

-- aircraft
-- serial, manufacture, plane
INSERT INTO Aircraft VALUES ('SN-001', 'Boeing', '737');
INSERT INTO Aircraft VALUES ('SN-002', 'Airbus', 'A320');
INSERT INTO Aircraft VALUES ('SN-003', 'Boeing', '787');
INSERT INTO Aircraft VALUES ('SN-004', 'Airbus', 'A380');

-- passengers
-- passport id, fname, lname, email, phone, miles
INSERT INTO Passenger VALUES ('P001', 'John', 'Doe', 'Jon.Doe@email.com', '555-1001', 12000);
INSERT INTO Passenger VALUES ('P002', 'Jalen', 'Brunson', 'Jalen.Brunson@email.com', '555-1002', 4500);
INSERT INTO Passenger VALUES ('P003', 'Karl', 'Towns', 'KAT@email.com', '555-1003', 32000);
INSERT INTO Passenger VALUES ('P004', 'Josh', 'Hart', 'Josh.Hart@email.com', '555-1004', 800);
INSERT INTO Passenger VALUES ('P005', 'Mikal', 'Bridges', 'Mikal.Bridges@email.com', '555-1005', 15500);

-- payments
-- id, amount, method
INSERT INTO Payment VALUES ('PAY-001', 349.99, 'Credit Card');
INSERT INTO Payment VALUES ('PAY-002', 729.50, 'Debit Card');
INSERT INTO Payment VALUES ('PAY-003', 1200.00, 'Credit Card');
INSERT INTO Payment VALUES ('PAY-004', 89.99, 'PayPal');
INSERT INTO Payment VALUES ('PAY-005', 2450.00, 'Credit Card');

-- Reservations
-- res-id, date, status, passport-id, payment-id
INSERT INTO Reservation VALUES ('RES-001', '2026-04-01', 'Confirmed', 'P001', 'PAY-001');
INSERT INTO Reservation VALUES ('RES-002', '2026-04-03', 'Confirmed', 'P002', 'PAY-002');
INSERT INTO Reservation VALUES ('RES-003', '2026-04-05', 'Cancelled', 'P003', 'PAY-003');
INSERT INTO Reservation VALUES ('RES-004', '2026-04-10', 'Confirmed', 'P004', 'PAY-004');
INSERT INTO Reservation VALUES ('RES-005', '2026-04-12', 'Pending',   'P005', 'PAY-005');

-- flights
-- flight id, call sign, departure, arrival, depature loc, arrival loc, times, status, serail num, arrival-code, depature-code, aircraft
INSERT INTO Flight VALUES ('FL-101', 'NYK101', '2026-05-01 08:00:00', '2026-05-01 11:30:00', 'JFK', 'LAX', 1, 'On Time', 'SN-001');
INSERT INTO Flight VALUES ('FL-102', 'GNG202', '2026-05-02 14:00:00', '2026-05-03 02:00:00', 'JFK', 'LHR', 1, 'On Time', 'SN-003');
INSERT INTO Flight VALUES ('FL-103', 'NYC303', '2026-05-03 09:00:00', '2026-05-03 11:15:00', 'LHR', 'CDG', 1, 'Delayed', 'SN-002');
INSERT INTO Flight VALUES ('FL-104', 'JBA404', '2026-05-05 06:30:00', '2026-05-05 08:45:00', 'ORD', 'JFK', 1, 'On Time', 'SN-001');
INSERT INTO Flight VALUES ('FL-105', 'GNY505', '2026-05-07 17:00:00', '2026-05-08 07:00:00', 'LAX', 'CDG', 1, 'On Time', 'SN-004');

-- Seats
-- seating no, seating row, flight_id, reservation-id, class, boaridng prio
INSERT INTO Seat VALUES ('1',  'A', 'FL-101', 'First',   1);
INSERT INTO Seat VALUES ('2',  'A', 'FL-101', 'First',   1);
INSERT INTO Seat VALUES ('10', 'B', 'FL-101', 'Business',2);
INSERT INTO Seat VALUES ('20', 'C', 'FL-101', 'Economy', 3);
INSERT INTO Seat VALUES ('10', 'B', 'FL-103', 'Business', 2);
INSERT INTO Seat VALUES ('1',  'A', 'FL-102', 'First',   1);
INSERT INTO Seat VALUES ('20', 'C', 'FL-102', 'Economy', 3);
INSERT INTO Seat VALUES ('1',  'A', 'FL-103', 'First',   1);
INSERT INTO Seat VALUES ('15', 'D', 'FL-103', 'Economy', 3);
INSERT INTO Seat VALUES ('1',  'A', 'FL-105', 'First',   1);
INSERT INTO Seat VALUES ('1',  'A', 'FL-104', 'First',   1);

-- Tickets
-- ticket id, issue date, price, resevation _id
INSERT INTO Ticket VALUES ('TKT-001', '2026-04-01', 349.99,  'RES-001');
INSERT INTO Ticket VALUES ('TKT-002', '2026-04-03', 729.50,  'RES-002');
INSERT INTO Ticket VALUES ('TKT-003', '2026-04-05', 1200.00, 'RES-003');
INSERT INTO Ticket VALUES ('TKT-004', '2026-04-10', 89.99,   'RES-004');
INSERT INTO Ticket VALUES ('TKT-005', '2026-04-12', 2450.00, 'RES-005');

-- Reservation_Flight (M:N junction)
-- res_id, flight_id
INSERT INTO Reservation_Flight VALUES ('RES-001', 'FL-101');
INSERT INTO Reservation_Flight VALUES ('RES-002', 'FL-102');
INSERT INTO Reservation_Flight VALUES ('RES-002', 'FL-103'); -- multi-leg trip
INSERT INTO Reservation_Flight VALUES ('RES-003', 'FL-103');
INSERT INTO Reservation_Flight VALUES ('RES-004', 'FL-104');
INSERT INTO Reservation_Flight VALUES ('RES-005', 'FL-105');

-- Ticket_Seat (1:1 junction)
-- ticket_id, seat, class, flight
INSERT INTO Ticket_Seat VALUES ('TKT-001', '1',  'A', 'FL-101');
INSERT INTO Ticket_Seat VALUES ('TKT-002', '1',  'A', 'FL-102');
INSERT INTO Ticket_Seat VALUES ('TKT-003', '15', 'D', 'FL-103');
INSERT INTO Ticket_Seat VALUES ('TKT-004', '1',  'A', 'FL-104');
INSERT INTO Ticket_Seat VALUES ('TKT-005', '1',  'A', 'FL-105');