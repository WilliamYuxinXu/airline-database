import pymysql.cursors
import decimal
import bcrypt
import datetime

def hashStr(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def checkPassword(password1, password2):
    return bcrypt.checkpw(password1.encode(), password2.encode())


def getFlights(cursor):
    query = 'SELECT * FROM flight ORDER BY departure_date, departure_time'
    cursor.execute(query)
    return cursor.fetchall() 

def searchFlights(cursor, flight_number	 = None, departure_date	 = None, departure_time = None, 
                  airplane_id = None, departure_airport = None, arrival_date = None, arrival_time = None,
                  arrival_airport = None, ticket_price = None, status = None, empty_seats = None, fetch_one = False,
                  passedDate = None, airline = None, past_days=None, future_days=None, departure_city=None, arrival_city=None):
    query = """
                SELECT flight.*, departure_city.city AS departure_city, arrival_city.city AS arrival_city FROM flight 
                JOIN airport departure_city ON departure_airport = departure_city.code 
                JOIN airport arrival_city ON arrival_airport = arrival_city.code 
            """
    parameters = []
    conditions = []
    if(departure_city is not None or arrival_city is not None):
        if departure_city:
            conditions.append('departure_city = %s')
            parameters.append(departure_city)
        if arrival_city:
            conditions.append('arrival_city = %s')
            parameters.append(arrival_city)
    if(flight_number is not None):
        if type(flight_number) == int:
            conditions.append('flight_number = %s')
            parameters.append(flight_number)
    if(departure_date is not None):
        if departure_date:
            conditions.append('departure_date = %s')
            parameters.append(departure_date)
    if(departure_time is not None):
        if departure_time:
            conditions.append('departure_time = %s')
            parameters.append(departure_time)
    if(airplane_id is not None):
        if len(airplane_id):
            conditions.append('airplane_id = %s')
            parameters.append(airplane_id)
    if(departure_airport is not None):
        if len(departure_airport):
            conditions.append('departure_airport = %s')
            parameters.append(departure_airport)
    if(arrival_date is not None):
        if len(arrival_date):
            conditions.append('arrival_date = %s')
            parameters.append(arrival_date)
    if(arrival_time is not None):
        if len(arrival_time):
            conditions.append('arrival_time = %s')
            parameters.append(arrival_time)
    if(arrival_airport is not None):
        if len(arrival_airport):
            conditions.append('arrival_airport = %s')
            parameters.append(arrival_airport)
    if(ticket_price is not None):
        if ticket_price:
            conditions.append('ticket_price =< %s')
            parameters.append(ticket_price)
    if(status is not None):
        if len(status):
            conditions.append('status = %s')
            parameters.append(status)
    if(empty_seats is not None):
        if empty_seats:
            conditions.append('empty_seats >= %s')
            parameters.append(empty_seats)
    if passedDate is not None:
        if passedDate:
            conditions.append('(departure_date < CURRENT_DATE() OR (departure_date = CURRENT_DATE() AND departure_time <= %s))')
            parameters.append('CURRENT_TIME()')
        else:
            conditions.append('NOT (departure_date < CURRENT_DATE() OR (departure_date = CURRENT_DATE() AND departure_time <= %s))')
            parameters.append('CURRENT_TIME()')
    if past_days is not None and future_days is not None:
        conditions.append('(departure_date BETWEEN DATE_SUB(CURDATE(), INTERVAL %s DAY)' )
        conditions.append('DATE_ADD(CURDATE(), INTERVAL %s DAY))')
        parameters.append(past_days)
        parameters.append(future_days)
    if airline is not None:
        query += ' NATURAL JOIN creates '
        conditions.append('airline_name = %s')
        parameters.append(airline)
    if len(conditions):
        query += ' WHERE '
    for i in range(len(conditions)):
        if(i > 0):
            query += ' AND '
        query += conditions[i]
    query += ' ORDER BY departure_date ASC, departure_time ASC'
    # print(query)
    cursor.execute(query, parameters)
    if fetch_one:
        return cursor.fetchone()
    return cursor.fetchall()
    
def changeTicketPrice(cursor, flight):
    # print("Finding Airline")
    query = 'SELECT airline_name FROM CREATES WHERE flight_number = %s AND departure_date = %s AND departure_time = %s'
    cursor.execute(query, (flight['flight_number'], flight['departure_date'], flight['departure_time']))
    airline = cursor.fetchone()['airline_name']
    query2 = 'SELECT number_of_seats FROM airplane WHERE airplane_id = %s AND airline_name = %s'
    # print("Finding Seats")
    cursor.execute(query2, (flight['airplane_id'], airline))
    maxSeats = int(cursor.fetchone()['number_of_seats'])
    if int(flight['empty_seats']) / maxSeats < .2:
        return flight['ticket_price'] * decimal.Decimal('1.25')
    return flight['ticket_price']

#hash unhashed passwords
def hashExistingPasswords(cursor, email, password):
    modify = 'UPDATE airline_staff SET password = %s WHERE username = %s'
    cursor.execute(modify, (password, email))


def getTicketsDateRange(cursor,  start_date, end_date, email=None, airline_name=None, count=None):
    query = """
        FROM buys JOIN ticket on buys.ticket_id = ticket.ticket_id 
    """
    if(email is not None):
        query += ' WHERE (buys.purchase_date BETWEEN %s AND %s) AND buys.email = %s'
        query = 'SELECT DISTINCT buys.email, SUM(ticket.current_price) AS total_price ' + query
        cursor.execute(query, (start_date, end_date, email))
        print(start_date, end_date)
        return cursor.fetchone()
    else:
        query += ' NATURAL JOIN flight NATURAL JOIN creates '
        query += ' WHERE (buys.purchase_date BETWEEN %s AND %s)  AND creates.airline_name = %s '
        if count is not None:
            query = 'SELECT DISTINCT buys.email, SUM(ticket.current_price) AS total_price, COUNT(*) AS trips ' + query
            query += ' GROUP BY email ORDER BY trips DESC'
        else:
            query = 'SELECT DISTINCT buys.email, SUM(ticket.current_price) AS total_price ' + query
            query += ' ORDER BY total_price DESC'
        cursor.execute(query, (start_date, end_date, airline_name))
        return cursor.fetchall()
    
def getMonthRanges(start_date=None, end_date=None):
    if end_date  is None:
        today = datetime.datetime.now()
    else:
        today = end_date
    if start_date is None:
        start_of_year = datetime.datetime(today.year, 1, 1)
    else:
        start_of_year = start_date
    current_month = today.replace(day=1)
    month_ranges = []
    while current_month >= start_of_year:
        end_of_month = current_month.replace(day=1) + datetime.timedelta(days=32)
        end_of_month = end_of_month.replace(day=1) - datetime.timedelta(days=1)
        if current_month.month == today.month and current_month.year == today.year:
            end_of_month = today
        start_of_month = current_month.replace(day=1)
        if start_date is not None:
            if current_month.month == start_of_year.month and current_month.year == start_of_year.year:
                start_of_month = start_date
        month_ranges.append((start_of_month, end_of_month))
        current_month = current_month.replace(day=1) - datetime.timedelta(days=1)
    return month_ranges[::-1]