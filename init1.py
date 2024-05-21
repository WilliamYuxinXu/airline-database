#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import customer as cus
import staff as st
import public as pu
import json
import datetime

#Initialize the app from Flask
app = Flask(__name__)

#endpoint names
CUSTOMER_EP = '/customer'
STAFF_EP = '/staff'
PUBLIC_EP = '/public'
LOGIN_EP = '/login'
FLIGHTS_EP = '/flights'
REGISTER_EP = '/register'
SEARCH_EP = '/search'
TICKET_EP = '/ticket'
AUTH_EP = 'Auth'
HOME_EP = '/home'
RESULTS_EP = 'Results'
BUY_EP = '/buy'
PAST_EP = '/past'
FUTURE_EP = '/future'
ADD_EP = '/add'
AIRPORT_EP = '/airport'
AIRPLANE_EP = '/airplane'
MAINTENANCE_EP = '/maintenance'
RATE_EP = '/rate'
CANCEL_EP = '/cancel'
MODIFY_EP = '/modify'
SPENDING_EP = '/spending'

#indicates of login is customer or staff
CUSTOMER = 'customer:'
CUSTOMER_LEN = len(CUSTOMER)
STAFF = 'staff:'
STAFF_LEN = len(STAFF)

MONTHS = {
	1: 'January',
	2: 'February',
	3: 'March',
	4: 'April',
	5: 'May',
	6: 'June',
	7: 'July',
	8: 'August',
	9: 'September',
	10: 'October',
	11: 'November',
	12: 'December',
}

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='airplane network',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Functions for just routes
@app.route('/')
def hello():
	return render_template('index.html')

@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')

@app.route(PUBLIC_EP + FLIGHTS_EP + SEARCH_EP)
def search_flights():
	return render_template('flight_search.html')

@app.route(CUSTOMER_EP + FLIGHTS_EP + SEARCH_EP)
def customer_search_flights():
	return render_template('flight_search.html', customer=session['username'][CUSTOMER_LEN:])

@app.route(STAFF_EP + FLIGHTS_EP + SEARCH_EP)
def staff_search_flights():
	return render_template('flight_search.html', staff=session['username'][STAFF_LEN:])

#Define route for login
@app.route(CUSTOMER_EP + LOGIN_EP)
def customerLogin():
	return render_template('customer_login.html')

#Define route for register
@app.route(CUSTOMER_EP + REGISTER_EP)
def customerRegister():
	return render_template('customer_register.html')

#Define route for login
@app.route(STAFF_EP + LOGIN_EP)
def staffLogin():
	return render_template('staff_login.html')

#Define route for register
@app.route(STAFF_EP + REGISTER_EP)
def staffRegister():
	return render_template('staff_register.html')


### PUBLICALLY AVALIABLE INFO

#Searches Flights
@app.route(PUBLIC_EP + FLIGHTS_EP + SEARCH_EP + RESULTS_EP, methods=['GET', 'POST'])
def flightSearchResults():
	#grabs information from the forms
	flight_number= request.form['flight_number']
	departure_date = request.form['departure_date']
	departure_time = request.form['departure_time']
	departure_airport = request.form['departure_airport']
	departure_city = request.form['departure_city']
	departure_date2 = request.form['arrival_date']
	departure_time2 = request.form['arrival_time']
	arrival_airport = request.form['arrival_airport']
	arrival_city = request.form['arrival_city']
	ticket_price = request.form['ticket_price']
	status = request.form['status']
	empty_seats = request.form['empty_seats']
	cursor = conn.cursor()
	if session.keys():
		user = session['username']
		if user[:STAFF_LEN] == STAFF:
			airline = st.getAirline(cursor, user[STAFF_LEN:])
			passed = request.form.get('has_passed')
			if passed is not None:
				if len(passed) == 0:
					passed = None
				elif passed == '1':
					passed = True
				else:
					passed = False
		else:
			passed = False
			airline = None
	else:
		passed = False
		airline = None
	data = pu.searchFlights(cursor=cursor, flight_number=flight_number, departure_date=departure_date, 
						 departure_time= departure_time, departure_airport= departure_airport, 
						 arrival_airport= arrival_airport,
						 ticket_price= ticket_price, status= status, empty_seats= empty_seats, passedDate = passed,
						 airline=airline, departure_city=departure_city, arrival_city=arrival_city
						 )
	print("Departure Date 2: ",departure_date2)
	for flight in data:
		flight['ticket_price'] = pu.changeTicketPrice(cursor, flight)
	if len(departure_date2) > 0:
		newData = []
		for val in data:
			returns = pu.searchFlights(cursor=cursor, departure_date=departure_date2, 
						 departure_time= departure_time2, departure_airport= val['arrival_airport'], 
						 arrival_airport= val['departure_airport'],
						 ticket_price= ticket_price, status= status, empty_seats= empty_seats, passedDate = passed,
						 airline=airline
						 )
			for flight in returns:
				flight['ticket_price'] = pu.changeTicketPrice(cursor, flight)
			for r in returns:
				temp = val
				temp['flight_number2'] = r['flight_number']
				temp['departure_date2'] = r['departure_date']
				temp['departure_time2'] = r['departure_time']
				temp['arrival_date2'] = r['arrival_date']
				temp['arrival_time2'] = r['arrival_time']
				temp['empty_seats2'] = r['empty_seats']
				temp['flight_number2'] = r['flight_number']
				temp['ticket_price'] = temp['ticket_price'] + r['ticket_price']
				temp['status2'] = r['status']
				temp['departure_airport2'] = r['departure_airport']
				temp['arrival_airport2'] = r['arrival_airport']
				temp['ticket_price2'] = r['ticket_price']
				temp['departure_city2'] = temp['arrival_city']
				temp['arrival_city2'] = temp['departure_city']
				newData.append(temp)
		data = newData
		roundTrip = True
	else:
		roundTrip = False

		
	cursor.close()
	print(session.keys())
	if session.keys():
		user = session['username']
		if user[:STAFF_LEN] == STAFF:
			return render_template('flight_search.html', flights=data, staff=session['username'][STAFF_LEN:], round=roundTrip)
		else:
			return render_template('flight_search.html', flights=data, customer=session['username'][CUSTOMER_LEN:], round=roundTrip)
	return render_template('flight_search.html', flights=data, round=roundTrip)



### EVERYTHING FOR CUSTOMERS GOES HERE


#Authenticates the login
@app.route(CUSTOMER_EP + LOGIN_EP + AUTH_EP, methods=['GET', 'POST'])
def customerLoginAuth():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']
	#cursor used to send queries
	cursor = conn.cursor()
	data = cus.validate(cursor, email, password)
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the customer
		#session is a built in
		session['username'] = CUSTOMER + email
		return redirect(url_for('customerHome', passed=None, message=None))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('customer_login.html', error=error)

#Authenticates the register
@app.route(CUSTOMER_EP + REGISTER_EP + AUTH_EP, methods=['GET', 'POST'])
def customerRegisterAuth():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	primary_phone = request.form['phone_number']
	building_number = request.form['building_number']
	street_name = request.form['street_name']
	apartment_number = request.form['apartment_number']
	city = request.form['city']
	state = request.form['state']
	zip_code = request.form['zip_code']
	passport_number = request.form['passport_number']
	passport_expiration = request.form['passport_expiration']
	passport_country = request.form['passport_country']
	date_of_birth = request.form['date_of_birth']
	password = pu.hashStr(password)
	#cursor used to send queries
	cursor = conn.cursor()
	#stores the results in a variable
	data = cus.exists(cursor, email)
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then customer exists
		error = "This customer already exists"
		cursor.close()
		return render_template('register_customer.html', error = error)
	else:
		cus.addUser(cursor, email, password, first_name, last_name, primary_phone, building_number, street_name, apartment_number, city, 
					   state, zip_code, passport_number, passport_expiration, passport_country, date_of_birth)
		conn.commit()
		cursor.close()
		return render_template('index.html')


@app.route(CUSTOMER_EP + HOME_EP + PAST_EP)
def customerHomePast():
	return redirect(url_for('customerHome', passed=True,  message="Viewing Past Flights"))

@app.route(CUSTOMER_EP + HOME_EP + FUTURE_EP)
def customerHomeFuture():
	return redirect(url_for('customerHome', message="Viewing Current Flights"))

@app.route(CUSTOMER_EP + HOME_EP)
def customerHome():
	passed = request.args.get('passed')
	message = request.args.get('message')
	username = session['username'][CUSTOMER_LEN:]
	cursor = conn.cursor()
	if passed is None:
		passed = False
	else:
		passed = True
	data1 = cus.findFlightByEmail(cursor, username, passed)
	cursor.close()
	return render_template('customer_home.html', username=username, flights=data1, passed=passed, message=message)

#buying ticket page
@app.route(CUSTOMER_EP + TICKET_EP, methods=['POST'])
def customerTicket():
	flight_number = request.form['flight_number']
	departure_date = request.form['departure_date']
	departure_time = request.form['departure_time']
	current_price = request.form['current_price']
	flight_number2 = request.form['flight_number2']
	departure_date2 = request.form['departure_date2']
	departure_time2 = request.form['departure_time2']
	current_price2 = request.form['current_price2']
	print(current_price)
	if not current_price:
		print("not price found")
	return render_template('customer_buy.html', flight_number=flight_number, departure_date=departure_date, 
						departure_time = departure_time, current_price = current_price, flight_number2=flight_number2, 
						departure_date2=departure_date2, departure_time2 = departure_time2, current_price2 = current_price2)

@app.route(CUSTOMER_EP + TICKET_EP + BUY_EP, methods=['GET', 'POST'])
def customerBuy():
	flight_number = request.form['flight_number']
	departure_date = request.form['departure_date']
	departure_time = request.form['departure_time']
	current_price = request.form['current_price']

	# this is for round trips 
	flight_number2 = request.form['flight_number2']
	departure_date2 = request.form['departure_date2']
	departure_time2 = request.form['departure_time2']
	current_price2 = request.form['current_price2']
	if len(current_price2) > 0:
		current_price = float(current_price) - float(current_price2)

	cursor = conn.cursor()
	email = request.form['email']
	date_of_birth = request.form['date_of_birth']
	card_type = request.form['card_type']
	card_number = request.form['card_number']
	name_on_card = request.form['name_on_card']
	expiration_date = request.form['expiration_date']
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	user_email = session['username'][CUSTOMER_LEN:]
	if not cus.seatAvaliable(cursor, flight_number, departure_date, 
						  departure_time) or (len(flight_number2) > 0 and cus.seatAvaliable(cursor, flight_number2, departure_date2, departure_time2) ):
		error = 'No Seats Avaliable'
		cursor.close()
		return render_template('customer_buy.html', flight_number=flight_number, departure_date=departure_date, 
						departure_time = departure_time, current_price = current_price, 
						flight_number2=flight_number2, departure_date2=departure_date2, 
						departure_time2 = departure_time2, current_price2 = current_price2, error=error)
	id = cus.createTicket(cursor=cursor, flight_number=flight_number, departure_date=departure_date,
				  departure_time=departure_time, email=email, first_name=first_name, last_name=last_name, 
				  date_of_birth=date_of_birth, current_price=current_price)
	conn.commit()
	cus.recordTransaction(cursor=cursor, ticket_id=id, email=user_email,card_type=card_type, card_number=card_number, 
					   name_on_card=name_on_card, expiration_date=expiration_date)
	conn.commit()
	cus.reserveSeat(cursor, flight_number, departure_date, departure_time, False)
	conn.commit()

	if flight_number2: # for reserving the round trip back flight
		id2 = cus.createTicket(cursor=cursor, flight_number=flight_number2, departure_date=departure_date2,
				  departure_time=departure_time2, email=email, first_name=first_name, last_name=last_name, 
				  date_of_birth=date_of_birth, current_price=current_price2)
		conn.commit()
		cus.recordTransaction(cursor=cursor, ticket_id=id2, email=user_email,card_type=card_type, card_number=card_number, 
						name_on_card=name_on_card, expiration_date=expiration_date)
		conn.commit()
		cus.reserveSeat(cursor, flight_number2, departure_date2, departure_time2, False)
		conn.commit()
		current_price += float(current_price2)

	cursor.close()
	purchased = 'Succesfully Bought a Ticket For: ' + first_name + ' ' + last_name
	return render_template('customer_buy.html', flight_number=flight_number, departure_date=departure_date, 
						departure_time = departure_time, current_price = current_price, 
						flight_number2=flight_number2, departure_date2=departure_date2, 
						departure_time2 = departure_time2, current_price2 = current_price2,purchased=purchased)

#buying ticket page
@app.route(CUSTOMER_EP + RATE_EP , methods=['POST', 'GET'])
def customerRating():
	flight_number = request.form['flight_number']
	departure_date = request.form['departure_date']
	departure_time = request.form['departure_time']
	rating = request.form['rating']
	comment = request.form['comment']
	cursor = conn.cursor()
	ret = cus.makeRating(cursor=cursor, flight_number=flight_number, email=session['username'][CUSTOMER_LEN:], 
					  departure_date=departure_date, departure_time=departure_time, rating=rating, comment=comment)
	
	if not ret:
		cursor.close()
		return redirect(url_for('customerHome', passed=True, message="Only One Rating Per Flight"))
	conn.commit()
	cursor.close()
	return redirect(url_for('customerHome', passed=True , message="Rating Recorded"))


#buying ticket refund
@app.route(CUSTOMER_EP + TICKET_EP + CANCEL_EP, methods=['POST'])
def customerTicketCancel():
	ticket_id = request.form['ticket_id']
	flight_number = request.form['flight_number']
	departure_date = request.form['departure_date']
	departure_time = request.form['departure_time']
	cursor = conn.cursor()
	if cus.check24Hrs(cursor, ticket_id):
		cus.delTicket(cursor, ticket_id)
		conn.commit()
		cus.reserveSeat(cursor=cursor, flight_number=flight_number, departure_date=departure_date, departure_time=departure_time,
				  addMode=True)
		conn.commit()
		return redirect(url_for('customerHome', message="Successfully Canceled Flight"))
	return redirect(url_for('customerHome', message="Cannot Cancel Flight"))


@app.route(CUSTOMER_EP + SPENDING_EP, methods=['GET', 'POST'])
def customerSpending():
	start_date = request.form.get('start_date')
	end_date = request.form.get('end_date')
	if start_date is not None and end_date is not None:
		start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
		end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
		if end_date < start_date:
			return render_template('customer_spending.html', error="End Date cannot be behind Start Date")
	cursor = conn.cursor()
	dates = pu.getMonthRanges(start_date, end_date)
	spending = []
	for date in dates:
		val = pu.getTicketsDateRange(cursor=cursor, start_date=date[0], end_date=date[1], 
										 email=session['username'][CUSTOMER_LEN:])
		if val['total_price'] is None:
			val['total_price'] = '0'
		val['month'] = MONTHS[date[0].month]
		val['year'] = date[0].year
		spending.append(val)
	if len(dates) > 0:
		total = pu.getTicketsDateRange(cursor=cursor, start_date=dates[0][0], end_date=dates[len(dates)  - 1][1], 
									email=session['username'][CUSTOMER_LEN:])['total_price']
	else:
		total = 0
		if start_date is not None and end_date is not None:
			val = {'total_price': '0',
			'month': MONTHS[start_date.month],
			'year': start_date.year}
			spending.append(val)
	if total is None:
		total = 0
	cursor.close()
	return render_template('customer_spending.html', data=spending, message=total)




### EVERYTHING FOR STAFF GOES HERE


#Authenticates the login
@app.route(STAFF_EP + LOGIN_EP + AUTH_EP, methods=['GET', 'POST'])
def staffLoginAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	data = st.validate(cursor, username, password)
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the staff
		#session is a built in
		session['username'] = STAFF + username
		return redirect(url_for('staffHome', past_days=0, future_days=30))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('staff_login.html', error=error)

#Authenticates the register
@app.route(STAFF_EP + REGISTER_EP + AUTH_EP, methods=['GET', 'POST'])
def staffRegisterAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']
	airline_name = request.form['airline_name']
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	primary_phone = request.form['phone_number']
	primary_email = request.form['email']
	date_of_birth = request.form['date_of_birth']

	#cursor used to send queries
	cursor = conn.cursor()
	#stores the results in a variable
	data = st.exists(cursor, username)
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then customer exists
		error = "This staff already exists"
		cursor.close()
		return render_template('staff_register.html', error = error)
	else:
		password = pu.hashStr(password)
		st.addUser(cursor, username, airline_name, password, first_name, last_name, date_of_birth, 
			  primary_email, primary_phone)
		conn.commit()
		cursor.close()
		return render_template('index.html')

@app.route(STAFF_EP + HOME_EP, methods=['POST', 'GET'])
def staffHome():
	username = session['username'][STAFF_LEN:] 
	cursor = conn.cursor() 
	airline = st.getAirline(cursor, username)
	past_days = request.args.get('past_days')
	future_days = request.args.get('future_days')
	if past_days is None and future_days is None:
		past_days = 0
		future_days = 30
	data1 = pu.searchFlights(cursor=cursor, airline=airline, past_days=past_days, future_days=future_days)
	# print(data1)
	cursor.close()
	print(past_days, future_days)
	if int(past_days) == 0:
		return render_template('staff_home.html', username=username, flights=data1, future=future_days )
	return render_template('staff_home.html', username=username, flights=data1, past=past_days)

@app.route(STAFF_EP + HOME_EP + PAST_EP, methods=['POST', 'GET'])
def staffHomePast():
	past_days = request.form.get('past_days')
	future_days = request.form.get('future_days')
	if past_days is None:
		past_days = 0
	if future_days is None:
		future_days = 0
	return redirect(url_for('staffHome', past_days=past_days, future_days=future_days))

@app.route(STAFF_EP + ADD_EP)
def staffAddPage():
	return render_template('staff_add.html')

@app.route(STAFF_EP + ADD_EP + FLIGHTS_EP)
def staffAddFlight():
	return render_template('staff_add.html', flight=True)

@app.route(STAFF_EP + ADD_EP + AIRPORT_EP)
def staffAddAirport():
	return render_template('staff_add.html', airport=True)

@app.route(STAFF_EP + ADD_EP + AIRPLANE_EP)
def staffAddAirplane():
	return render_template('staff_add.html', airplane=True)

@app.route(STAFF_EP + ADD_EP + MAINTENANCE_EP)
def staffAddMaintenance():
	return render_template('staff_add.html', maintenance=True)

@app.route(STAFF_EP + ADD_EP + AIRPLANE_EP + ADD_EP, methods=['POST'])
def staffAddAirplaneSubmit():
	cursor = conn.cursor()
	airplane_id= request.form['airplane_id']
	number_of_seats = request.form['number_of_seats']
	manufacturer = request.form['manufacturer']
	model_number = request.form['model_number']
	manufacturing_date = request.form['manufacturing_date']
	airline_name = st.getAirline(cursor, session['username'][STAFF_LEN:])
	error, success = st.addAirplane(cursor, airplane_id, airline_name, number_of_seats, manufacturer, model_number, 
								manufacturing_date)
	if success:
		conn.commit()
		st.updateAirplaneManufacturing(cursor)
		conn.commit()
		data = st.getAllAirplane(cursor, airline_name)
		cursor.close()
		return render_template('staff_add.html', airplane=True, submit = 'Added Airplane', airplanes=data)
	else:
		cursor.close()
		return render_template('staff_add.html', airplane=True, submit = error)
	
@app.route(STAFF_EP + FLIGHTS_EP + MODIFY_EP, methods=['POST'])
def staffModifyFlightStatus():
	cursor = conn.cursor()
	flight_number= request.form['flight_number']
	departure_date = request.form['departure_date']
	departure_time = request.form['departure_time']
	status = request.form['status']
	future_days = request.form['future_days']
	print(flight_number, departure_date, departure_time)
	ret = st.changeStatus(cursor=cursor, flight_number=flight_number, departure_date=departure_date, 
				 departure_time=departure_time, status=status)
	print(ret)
	conn.commit()
	return redirect(url_for('staffHome', past_days=0, future_days=future_days))
	

@app.route(STAFF_EP + ADD_EP + AIRPORT_EP + ADD_EP, methods=['POST'])
def staffAddAirportSubmit():
	cursor = conn.cursor()
	code= request.form['code']
	name = request.form['name']
	city = request.form['city']
	country = request.form['country']
	number_of_terminals = request.form['number_of_terminals']
	type = request.form['type']
	error, success = st.addAirport(cursor, code, name, city, country, number_of_terminals, type)
	if success:
		conn.commit()
		cursor.close()
		return render_template('staff_add.html', airport=True, submit = 'Added Airport')
	else:
		cursor.close()
		return render_template('staff_add.html', airport=True, submit = error)

@app.route(STAFF_EP + ADD_EP + FLIGHTS_EP + ADD_EP, methods=['POST'])
def staffAddFlightSubmit():
	cursor = conn.cursor()
	flight_number= request.form['flight_number']
	departure_date = request.form['departure_date']
	departure_time = request.form['departure_time']
	departure_airport = request.form['departure_airport']
	airplane_id = request.form['airplane_id']
	arrival_date = request.form['arrival_date']
	arrival_time = request.form['arrival_time']
	arrival_airport = request.form['arrival_airport']
	ticket_price = request.form['ticket_price']
	status = request.form['status']
	if not st.checkAirportType(cursor, arrival_airport, departure_airport):
		cursor.close()
		return render_template('staff_add.html', flight=True, submit = "Something wrong with airports")
	airline_name = st.getAirline(cursor, session['username'][STAFF_LEN:])
	error, success =st.addFlight(cursor=cursor, flight_number=flight_number, departure_date=departure_date, departure_time=departure_time,
			  departure_airport=departure_airport, airplane_id=airplane_id, arrival_date=arrival_date, arrival_time=arrival_time, 
			  arrival_airport=arrival_airport, ticket_price=ticket_price, status=status, username=session['username'][STAFF_LEN:])
	if success:
		conn.commit()
		error2, success2 = st.addCreates(cursor=cursor, airline_name=airline_name, flight_number=flight_number, departure_date=departure_date,
				departure_time=departure_time)
		if(not success2):
			cursor.close()
			return render_template('staff_add.html', flight=True, submit = error2)
		conn.commit()
		cursor.close()
		return render_template('staff_add.html', flight=True, submit = 'Added Flight')
	else:
		cursor.close()
		return render_template('staff_add.html', flight=True, submit = error)

@app.route(STAFF_EP + ADD_EP + MAINTENANCE_EP + ADD_EP, methods=['POST'])
def staffAddMaintenanceSubmit():
	cursor = conn.cursor()
	airplane_id = request.form['airplane_id']
	start_date = request.form['start_date']
	end_date = request.form['end_date']
	start_time = request.form['start_time']
	end_time = request.form['end_time']
	airline_name = st.getAirline(cursor, session['username'][STAFF_LEN:])
	error, success =st.addMaintenance(cursor=cursor, airplane_id=airplane_id, start_date=start_date, start_time=start_time, end_date=end_date,
								   end_time=end_time, airline_name=airline_name)
	if success:
		conn.commit()
		cursor.close()
		return render_template('staff_add.html', maintenance=True, submit = 'Added Maintenance')
	else:
		cursor.close()
		return render_template('staff_add.html', maintenance=True, submit = error)
	
@app.route(STAFF_EP + RATE_EP, methods=['POST'])
def staffViewRatings():
	cursor = conn.cursor()
	flight_number= request.form['flight_number']
	departure_date = request.form['departure_date']
	departure_time = request.form['departure_time']
	past_days = request.form['past_days']
	average_rating = st.getAverageRating(cursor, flight_number=flight_number, departure_date=departure_date, departure_time=departure_time)
	data = st.getAllRatings(cursor, flight_number=flight_number, departure_date=departure_date, departure_time=departure_time)
	return render_template('staff_comments.html', ratings=data, average_rating=average_rating, flight_number=flight_number, past=past_days)
	
@app.route(STAFF_EP + SPENDING_EP, methods=['POST', 'GET'])
def staffEarnings():
	cursor = conn.cursor()
	range = pu.getMonthRanges()
	start_date = range[0][0]
	end_date = range[len(range) - 1][1]
	airline = st.getAirline(cursor, session['username'][STAFF_LEN:])
	customers = pu.getTicketsDateRange(cursor=cursor, start_date=start_date, end_date=end_date, 
										 airline_name=airline, count=True)
	print(customers)
	for val in customers:
		if val['total_price'] is None:
			val['total_price'] = '0'
	last_month = st.getRevenue(cursor, airline)
	last_year = st.getRevenue(cursor, airline, True)
	if not last_year:
		last_year = '0'
	if not last_month:
		last_month = '0'
	cursor.close()
	return render_template('staff_spending.html', data=customers,  month=last_month, year=last_year)


@app.route(STAFF_EP + FLIGHTS_EP + SPENDING_EP, methods=['POST', 'GET'])
def staffCustomerFlights():
	cursor = conn.cursor()
	customer = request.form.get('email')
	data1 = st.findFlightByEmail(cursor, customer)
	cursor.close()
	return render_template('staff_customer_flight.html', flights=data1)


@app.route(STAFF_EP + CUSTOMER_EP, methods=['POST', 'GET'])
def staffCustomerOnFlight():
	cursor = conn.cursor()
	flight_number = request.form.get('flight_number')
	departure_date = request.form.get('departure_date')
	departure_time = request.form.get('departure_time')
	data1 = st.getCustomersByFlight(cursor, flight_number, departure_date, departure_time)
	cursor.close()
	return render_template('staff_view_customers.html', data=data1, flight=flight_number)


app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
