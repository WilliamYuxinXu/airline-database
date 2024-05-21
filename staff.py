import pymysql.cursors
import public as pu
import datetime

#checks if staff already exists
def exists(cursor, username):
    query = 'SELECT * FROM airline_staff WHERE username = %s'
    cursor.execute(query, (username))
    return cursor.fetchone()

#checks if airline exists
def airlineExists(cursor, airline_name):
    query = 'SELECT * FROM airline WHERE username = %s'
    cursor.execute(query, (airline_name))
    return cursor.fetchone()

#adds staff to the database
def addUser(cursor, username, airline_name, password, first_name, last_name, date_of_birth, primary_email, primary_phone):
    ins = 'INSERT INTO airline_staff VALUES(%s , %s, %s,%s, %s , %s , %s, %s)'
    cursor.execute(ins, (username, airline_name, password, first_name, last_name, date_of_birth, primary_email, primary_phone))

#checks credentials for staff when logging in
def validate(cursor, username, password):
    query = 'SELECT * FROM airline_staff WHERE username = %s'
    cursor.execute(query, (username))
	#stores the results in a variable
    val =  cursor.fetchone()
    if val is None:
        return None
    if pu.checkPassword(password, val['password']):
        return val
    return None


def getAll(cursor):
    query = 'SELECT * FROM airline_staff'
    cursor.execute(query)
    return cursor.fetchall()

def getAirline(cursor, username):
    query = 'SELECT airline_name from airline_staff WHERE username = %s'
    cursor.execute(query, (username))
    return cursor.fetchone()['airline_name']

def getAirplane(cursor, id, airline):
    query = 'SELECT * from airplane WHERE airplane_id = %s AND airline_name = %s'
    cursor.execute(query, (id, airline))
    return cursor.fetchone()

def getAllAirplane(cursor, airline):
    query = 'SELECT * from airplane WHERE airline_name = %s'
    cursor.execute(query, (airline))
    return cursor.fetchall()

def addFlight(cursor, flight_number, departure_date, departure_time, airplane_id, departure_airport, arrival_date, arrival_time, 
              arrival_airport, ticket_price, status, username=None):
    if(departure_date > arrival_date):
        return "Deprature Date is past Arrival Date", False
    if(departure_date == arrival_date and departure_time > arrival_time):
        return "Deprature Time is past Arrival Time", False
    if username is not None:
        airline = getAirline(cursor, username)
        print(airline)
    if not checkUnderMaintenance(cursor=cursor, airplane_id=airplane_id, airline_name=airline, departure_date=departure_date, 
                             departure_time=departure_time, arrival_date=arrival_date, arrival_time=arrival_time):
        return "Airplane is under Maintenance during that time", False
    
    airplane = getAirplane(cursor, airplane_id, airline)
    if airplane is None:
        return "This Airplane does not exist", False
    seats_empty = getAirplane(cursor, airplane_id, airline)['number_of_seats']
    try:
        insert = 'INSERT INTO flight VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(insert, (flight_number, departure_date, departure_time, airplane_id, departure_airport, arrival_date, arrival_time, 
                arrival_airport, ticket_price, status, seats_empty))
    except:
        return "SQL Exception, Airport cannot be found or invalid Ticket Price", False
    return "success", True

def addCreates(cursor, airline_name, flight_number, departure_date, departure_time):
    try:
        insert = 'INSERT INTO creates VALUES(%s, %s, %s, %s)'
        cursor.execute(insert, (airline_name, flight_number, departure_date, departure_time))
    except:
        return "SQL Exception, Cannot Add to Creates", False
    return "success", True

def addAirport(cursor, code, name, city, country, number_of_terminals, type):
    try:
        insert = 'INSERT INTO airport VALUES(%s, %s, %s, %s, %s, %s)'
        cursor.execute(insert, (code, name, city, country, number_of_terminals,type))
    except:
        return "SQL Exception, Something went really wrong", False
    return "success", True


def addAirplane(cursor, airplane_id, airline_name, number_of_seats, manufacturer, model_number, 
                manufacturing_date):
    if(datetime.datetime.strptime(manufacturing_date, '%Y-%m-%d').date() > datetime.datetime.now().date()):
        return "Manufacturing date is in the Future", False
    try:
        insert = 'INSERT INTO airplane VALUES(%s, %s, %s, %s, %s, %s, 0)'
        cursor.execute(insert, (airplane_id, airline_name, number_of_seats, manufacturer, model_number, 
                manufacturing_date))
    except:
        return "SQL Exception, Something went really wrong", False
    return "success", True


def updateAirplaneManufacturing(cursor):
    try:
        update = 'UPDATE airplane SET age = TIMESTAMPDIFF(YEAR, manufacturing_date, CURRENT_DATE())'
        cursor.execute(update)
    except:
        return False
    return True


def addMaintenance(cursor, airplane_id, airline_name, start_date, end_date, start_time, end_time):
    if(datetime.datetime.strptime(start_date, '%Y-%m-%d').date() < datetime.datetime.now().date()):
        return "Maintenance date is in the Past", False
    if start_date > end_date or (start_date == end_date and start_time > end_date):
        return "Ends before it even starts", False
    try:
        if not checkMaintenanceConflictsWithFlight(cursor=cursor, airplane_id=airplane_id, airline_name=airline_name, 
                                               start_date=start_date, start_time=start_time, end_date=end_date, end_time=end_time):
            return "This Maintenance Conflicts with a current flight", False
        insert = 'INSERT INTO maintenance_procedure VALUES(%s, %s, %s, %s, %s, %s)'
        cursor.execute(insert, (airplane_id, start_date, end_date, start_time, end_time, airline_name))
    except:
        return "SQL Error, probably because flight doesn't exist", False
    return "", True


def checkUnderMaintenance(cursor, airplane_id, airline_name, departure_date, departure_time, arrival_date, arrival_time):
    query = """
    SELECT * FROM maintenance_procedure 
    WHERE airplane_id = %s 
    AND airline_name = %s 
    AND (
        start_date <= %s 
        AND end_date >= %s
    )
    AND (
        (start_date = %s AND end_date = %s AND end_time >= %s AND start_time <= %s)
        OR (start_date < %s AND end_date = %s AND end_time >= %s)
        OR (start_date = %s AND end_date > %s AND start_time <= %s)
        OR (start_date < %s AND end_date > %s)
        OR (start_date = %s AND end_date = %s AND start_time <= %s));
    """
    try:
        cursor.execute(query, (airplane_id, airline_name, arrival_date, departure_date, arrival_date, departure_date, departure_time, 
                            arrival_time, arrival_date, departure_date, departure_time, arrival_date, departure_date, 
                            arrival_time, arrival_date, departure_date, arrival_date, departure_date, departure_time))
        if cursor.fetchone() is None:
            print("Not Under Maintenmence")
            return True
    except Exception as inst:
        print(inst)
        return False
    return False

def checkMaintenanceConflictsWithFlight(cursor, airplane_id, airline_name, start_date, start_time, end_date, end_time):
    query = """
    SELECT * FROM flight
    NATURAL JOIN creates
    WHERE airplane_id = %s 
    AND airline_name = %s 
    AND (
        (departure_date < %s OR (departure_date = %s AND departure_time <= %s))
        AND
        (arrival_date > %s OR (arrival_date = %s AND arrival_time >= %s))
    );
    """
    try:
        cursor.execute(query, (airplane_id, airline_name, end_date, end_date, end_time,
                               start_date, start_date, start_time))
        if cursor.fetchone() is None:
            print("Could Not Find a Conflict")
            return True
        return False
    except Exception as inst:
        print(inst)
        return False

def checkAirportType(cursor, code1, code2):
    query = 'SELECT type FROM airport WHERE code = %s'
    cursor.execute(query, (code1))
    ret = cursor.fetchone()
    cursor.execute(query, (code2))
    ret2 = cursor.fetchone()
    if ret is not None and ret2 is not None:
        if ret['type'] == 'Domestic':
            if ret2['type'] == 'Domestic' or ret2['type'] == 'Both':
                return ret['country'] == ret2['country']
            elif ret2['type'] == 'International':
                return False
        elif ret['type'] == 'International':
            if ret2['type'] == 'International' or ret2['type'] == 'Both':
                return ret['country'] != ret2['country']
            elif ret2['type'] == 'Domestic':
                return False
        elif ret['type'] == 'Both':
            if ret2['type'] == 'Both':
                return True
            elif ret2['type'] == 'International':
                return ret['country'] != ret2['country']
            elif ret2['type'] == 'Domestic':
                return ret['country'] == ret2['country']
    return False

def changeStatus(cursor, flight_number, departure_date, departure_time, status):
    modify = 'UPDATE flight SET status = %s WHERE flight_number = %s AND departure_date = %s AND departure_time = %s'
    try:
        if status == 'On-Time':
            cursor.execute(modify, ('Delayed', flight_number, departure_date, departure_time))
        else:
            cursor.execute(modify, ('On-Time', flight_number, departure_date, departure_time))
        return True
    except Exception as inst:
        print(inst)
        return False
    
def getAllRatings(cursor, flight_number, departure_date, departure_time):
    try:
        query= 'SELECT * FROM rates WHERE flight_number = %s AND departure_date = %s AND departure_time = %s '
        cursor.execute(query, (flight_number, departure_date, departure_time))
        return cursor.fetchall()
    except:
        return False
    
def getAverageRating(cursor, flight_number, departure_date, departure_time):
    query = 'SELECT AVG(rating) AS average_rating FROM rates WHERE flight_number= %s AND departure_date = %s AND departure_time = %s'
    try:
        cursor.execute(query, (flight_number, departure_date, departure_time))
        return cursor.fetchone()['average_rating']
    except Exception as inst:
        return False
    
def getRevenue(cursor, airline_name, year=False): #if year is false then get last month
    query = """
        SELECT SUM(ticket.current_price) AS total_price FROM buys JOIN ticket on buys.ticket_id = ticket.ticket_id 
         NATURAL JOIN flight NATURAL JOIN creates  WHERE (buys.purchase_date BETWEEN %s AND %s)  AND creates.airline_name = %s 
         ORDER BY total_price DESC
    """
    dates = pu.getMonthRanges()
    if year:
        start_date =  dates[0][0].replace(day=1, month=1)
        last_year = start_date.year - 1
        start_date = start_date.replace(year=last_year)
        end_date = start_date - datetime.timedelta(days=1)
        end_date = end_date.replace(year = last_year)
    else:
        start_date =  dates[len(dates) - 1][0].replace(day=1)
        end_date = start_date - datetime.timedelta(days=1)
        start_date = end_date.replace(day=1)
    print(start_date, end_date)
    cursor.execute(query, (start_date, end_date, airline_name))
    return cursor.fetchone()['total_price']


def findFlightByEmail(cursor, email):
    query = 'SELECT DISTINCT flight_number, departure_date, departure_time FROM ticket JOIN buys ON ticket.ticket_id = buys.ticket_id WHERE buys.email = %s'
    cursor.execute(query, (email))
    res = cursor.fetchall()
    flights = []
    for val in res:
        temp = pu.searchFlights(cursor=cursor, flight_number=val['flight_number'], departure_date=val['departure_date'],
                                        departure_time=val['departure_time'], fetch_one=True)
        if temp is not None:
            flights.append(temp)
    return flights

def getCustomersByFlight(cursor, flight_number, departure_date, departure_time):
    query = """
    SELECT DISTINCT customer.email, customer.first_name, customer.last_name FROM customer JOIN buys ON customer.email = buys.email 
    JOIN ticket ON buys.ticket_id = ticket.ticket_id WHERE ticket.flight_number = %s AND ticket.departure_date = %s AND ticket.departure_time = %s
    """
    cursor.execute(query, (flight_number, departure_date, departure_time))
    return cursor.fetchall()