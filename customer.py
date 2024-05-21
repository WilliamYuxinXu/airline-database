import pymysql.cursors
import public as pu
import random
import datetime
import uuid
import decimal
import json

# checks if user already exists
def exists(cursor, email):
    query = 'SELECT * FROM customer WHERE email = %s'
    cursor.execute(query, (email))
    return cursor.fetchone()

#adds a user with the given parameters
def addUser(cursor, email, password, first_name, last_name, primary_phone, building_number, street_name, apartment_number, city, 
					   state, zip_code, passport_number, passport_expiration, passport_country, date_of_birth):
    if not apartment_number:
        apartment_number = None
    ins = 'INSERT INTO customer VALUES(%s, %s , %s , %s, %s, %s, %s , %s , %s, %s,%s, %s , %s , %s, %s)'
    cursor.execute(ins, (email, password, first_name, last_name, primary_phone, building_number, street_name, apartment_number, city, 
					   state, zip_code, passport_number, passport_expiration, passport_country, date_of_birth))

#checks the credentials of the customer for login
def validate(cursor, email, password):
    query = 'SELECT * FROM customer WHERE email = %s'
    cursor.execute(query, (email))
	#stores the results in a variable
    val = cursor.fetchone()
    if pu.checkPassword(password, val['password']):
        return val
    return None

def findFlightByEmail(cursor, email, passed=None):
    query = 'SELECT DISTINCT * FROM ticket JOIN buys ON ticket.ticket_id = buys.ticket_id WHERE buys.email = %s'
    cursor.execute(query, (email))
    res = cursor.fetchall()
    # print(res)
    flights = []
    for val in res:
        temp = pu.searchFlights(cursor=cursor, flight_number=val['flight_number'], departure_date=val['departure_date'],
                                        departure_time=val['departure_time'], fetch_one=True, passedDate=passed)
        if temp is not None:
            temp['ticket_id'] = val['ticket_id']
            temp['name'] = val['first_name'] + ' ' + val['last_name']
            # print(temp)
            flights.append(temp)
    return flights

#creates a ticket, makes sure the id is unique
def createTicket(cursor, flight_number, departure_date, departure_time, email, first_name,
                 last_name, date_of_birth, current_price):
    id = str(uuid.uuid4()) # generates ticket id, basically impossible to get a duplicate
    ins = 'INSERT INTO ticket (ticket_id, flight_number, departure_date, departure_time, email, first_name, last_name, date_of_birth, current_price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(ins, (id, flight_number, departure_date, departure_time, email, first_name,
                 last_name, date_of_birth, current_price))
    return id

#creates a ticket, and stores a transaction record
def recordTransaction(cursor, ticket_id, email, card_type, card_number, name_on_card, expiration_date):

    #gets transaction times/date
    current_date = datetime.datetime.now().date()
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")

    # Now execute the INSERT INTO buys statement
    ins = 'INSERT INTO buys (ticket_id, email, card_type, card_number, name_on_card, expiration_date, purchase_date, purchase_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(ins, (ticket_id, email, card_type, card_number, name_on_card, expiration_date, current_date, current_time))

    return id

def reserveSeat(cursor, flight_number, departure_date, departure_time, addMode): #add = True: +1, False: -1
    if addMode:
        ins = 'UPDATE flight SET empty_seats = empty_seats + 1 WHERE flight_number = %s AND departure_date = %s AND departure_time = %s'
    else:
        ins = 'UPDATE flight SET empty_seats = empty_seats - 1 WHERE flight_number = %s AND departure_date = %s AND departure_time = %s'
    cursor.execute(ins, (flight_number, departure_date, departure_time))


def seatAvaliable(cursor, flight_number, departure_date, departure_time):
    flight = pu.searchFlights(cursor=cursor, flight_number=flight_number, departure_date=departure_date, departure_time=departure_time, 
                              fetch_one=True)
    print(flight_number, departure_date, departure_time)
    if(flight is None):
        print("cannot find flight")
    seats = int(flight['empty_seats'])
    print(seats)
    return seats > 0

def getAll(cursor):
    query = 'SELECT * FROM customer'
    cursor.execute(query)
    return cursor.fetchall()

def makeRating(cursor, email, flight_number, departure_date, departure_time, rating, comment):
    try:
        if(getRatings(cursor, flight_number, departure_date, departure_time, email)):
            return False
        insert = 'INSERT INTO rates VALUES(%s, %s, %s, %s, %s, %s)'
        cursor.execute(insert, (email, flight_number, departure_date, departure_time, rating, comment))
        return True
    except Exception as inst:
        print(inst)
        return False
    
def getRatings(cursor, flight_number, departure_date, departure_time, email = None):
    try:
        query= 'SELECT * FROM rates WHERE flight_number = %s AND departure_date = %s AND departure_time = %s '
        if email is None:
            cursor.execute(query, (flight_number, departure_date, departure_time))
        else:
            query += ' AND email = %s'
            cursor.execute(query, (flight_number, departure_date, departure_time, email))
        return cursor.fetchone()
    except:
        return False
    
def check24Hrs(cursor, ticket_id):
    try:
        print("Ticket ID: ", ticket_id)
        query="""SELECT  ticket_id, TIMESTAMPDIFF(HOUR, CONCAT(purchase_date, ' ', purchase_time), NOW()) 
        AS hours_passed FROM buys WHERE ticket_id = %s HAVING  hours_passed <= 24;"""
        cursor.execute(query, (ticket_id))
        return cursor.fetchone() is not None
    except Exception as inst:
        print(inst)
        return False

def delTicket(cursor, ticket_id):
    try:
        delete= "DELETE FROM ticket WHERE ticket_id = %s"
        cursor.execute(delete, (ticket_id))
        return True
    except Exception as inst:
        print(inst)
        return False