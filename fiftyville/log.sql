-- Keep a log of any SQL queries you execute as you solve the mystery.

SELECT * FROM crime_scene_reports WHERE year = 2021 AND month = 7 AND day = 28 AND street LIKE "Humphrey Street";
-- Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
-- Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.
-- id = 295

SELECT name, transcript FROM interviews WHERE year = 2021 AND month = 7 AND day = 28;
-- | Ruth    |  Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
-- If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.
-- | Eugene  | I don't know the thief's name, but it was someone I recognized.
-- Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.
-- | Raymond | As the thief was leaving the bakery, they called someone who talked to them for less than a minute.
-- In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
-- The thief then asked the person on the other end of the phone to purchase the flight ticket.

SELECT minute, activity, license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10
AND minute >  15 AND minute < 25 ORDER BY minute ASC;
--+--------+----------+---------------+
--| minute | activity | license_plate |
--+--------+----------+---------------+
--| 16     | exit     | 5P2BI95       |
--| 18     | exit     | 94KL13X       |
--| 18     | exit     | 6P58WS2       |
--| 19     | exit     | 4328GD8       |
--| 20     | exit     | G412CB7       |
--| 21     | exit     | L93JTIZ       |
--| 23     | exit     | 322W7JE       |
--| 23     | exit     | 0NTHK55       |
--+--------+----------+---------------+

SELECT * FROM atm_transactions LIMIT 5;
-- -> Table begutachten

SELECT account_number, transaction_type, amount FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND transaction_type = "withdraw" AND atm_location = "Leggett Street";
--+----------------+------------------+--------+
--| account_number | transaction_type | amount |
--+----------------+------------------+--------+
--| 28500762       | withdraw         | 48     |
--| 28296815       | withdraw         | 20     |
--| 76054385       | withdraw         | 60     |
--| 49610011       | withdraw         | 50     |
--| 16153065       | withdraw         | 80     |
--| 25506511       | withdraw         | 20     |
--| 81061156       | withdraw         | 30     |
--| 26013199       | withdraw         | 35     |
--+----------------+------------------+--------+

SELECT caller, receiver, duration FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60;
--+----------------+----------------+----------+
--|     caller     |    receiver    | duration |
--+----------------+----------------+----------+
--| (130) 555-0289 | (996) 555-8899 | 51       |
--| (499) 555-9472 | (892) 555-8872 | 36       |
--| (367) 555-5533 | (375) 555-8161 | 45       |
--| (499) 555-9472 | (717) 555-1342 | 50       |
--| (286) 555-6063 | (676) 555-6554 | 43       |
--| (770) 555-1861 | (725) 555-3243 | 49       |
--| (031) 555-6622 | (910) 555-3251 | 38       |
--| (826) 555-1652 | (066) 555-9701 | 55       |
--| (338) 555-6650 | (704) 555-2131 | 54       |
--+----------------+----------------+----------+

-- Next: assign people to requests
SELECT id, name FROM people where license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10
AND minute >  15 AND minute < 25);

SELECT people.id, people.name FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE year = 2021 AND month = 7 AND day = 28 AND transaction_type = "withdraw" AND atm_location = "Leggett Street";

SELECT people.id, people.name FROM people
JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60;

-- Additionally search for people in first flight
SELECT people.name FROM people
JOIN passengers ON passengers.passport_number = people.passport_number
WHERE passengers.flight_id IN(
    SELECT flights.id FROM flights
    JOIN airports ON airports.id = flights.origin_airport_id
    WHERE flights.year = 2021 AND flights.month = 7 AND flights.day = 29 AND airports.city LIKE "Fiftyville" ORDER BY flights.hour, flights.minute LIMIT 1
);

-- Next: combine requests
SELECT people.name FROM people WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10
AND minute > 15 AND minute < 25)
AND people.name IN(
    SELECT people.name FROM people
    JOIN bank_accounts ON people.id = bank_accounts.person_id
    JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
    WHERE year = 2021 AND month = 7 AND day = 28 AND transaction_type = "withdraw" AND atm_location = "Leggett Street")
AND people.name IN(
    SELECT people.name FROM people
    JOIN phone_calls ON people.phone_number = phone_calls.caller
    WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60)
AND people.name IN(
    SELECT people.name FROM people
    JOIN passengers ON passengers.passport_number = people.passport_number
    WHERE passengers.flight_id IN(
        SELECT flights.id FROM flights
        JOIN airports ON airports.id = flights.origin_airport_id
        WHERE flights.year = 2021 AND flights.month = 7 AND flights.day = 29 AND airports.city LIKE "Fiftyville" ORDER BY flights.hour, flights.minute LIMIT 1
    )
);

--> Thief: Bruce

-- get destination:
SELECT city FROM airports
JOIN flights ON airports.id = flights.destination_airport_id
JOIN passengers ON flights.id = passengers.flight_id
JOIN people ON people.passport_number = passengers.passport_number
WHERE people.name = "Bruce"
-->The city the thief ESCAPED TO: New York City

-- get ACCOMPLICE
SELECT people.name FROM people
JOIN phone_calls ON phone_calls.receiver = people.phone_number
WHERE phone_calls.caller IN (SELECT people.phone_number FROM people WHERE people.name = "Bruce")
AND phone_calls.duration < 60 AND phone_calls.year = 2021 AND phone_calls.month = 7 AND phone_calls.day = 28;
-- The ACCOMPLICE is: Robin