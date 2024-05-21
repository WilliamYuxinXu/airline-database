To Run:
    1. Have xampp appache and mysql started 
    2. python init1.py
    3. click the given link: http://127.0.0.1:5000

A list of files and uses are found under file_list.txt

The following are the applications of the website. 

Home Page:
    Here you can have 3 procedues, for the public, for customers, and for staff
    Public:
        click "Search Flights" link, here you can search for future flights from the flight table
        Query: This will run public.searchFlights(), which will add 'WHERE' conditions based on what field on the form are filled.
    
    Customer/Staff:
        you can either click on "Register" to create an account with the given inforamtion or "Login" to fill in the details
        Query: This will run a query to check if the account already exists (customer.exists(), staff.exists()), then will insert into
            the database the fields given (customer.addUser(), staff.addUser()) 

    Existing Accounts/Airlines:
        existing staff login: Username: bobby, Password: fbi
        existing customer login: Username: abc@gmail.com, Password: abc
        existing airlines: 'Jet Blue', 'a'

Customer Home:
    See Current/Cancel Flights: Here you can see your upcomming trips. You can cancel any flight if purchased within 24 hours 
    by clicking the "Cancel Flight" button in the row of the flight
        Query: for finding flights, customer.findFlightByEmail() runs a query that joins customer on buys to find flights, and searches flights using
            public.searchFlights(). For canceling flights, it will use customer.check24Hr() to run a query to see if the ticket was bought within 24 hrs, 
            then customer.delTicket() to delete the ticket from the ticket table and customer.reserveSeat() modify the flight to return the empty seat

    Search Flights/Buy Tickets: you can click on the search flights button to search for future flights with more information that public 
    searches. One column will allow you to buy tickets of the flight, which will take you to a form to purchase a ticket.
        Query: for flights users public.searchFlights(), and buying tickets uses customer.seatAvaliable() run a query to see if the flight has seats left, 
            otherwise a ticket will be inserted using customer.createTicket() and a buys will be inserted using customer.recordTransaction

    See Past Flights/Rating: clicking "See Past Flights" button will display your past flights, the "Cancel Flight" button is 
    replaced with a submit rating. You can return to current flights with the button "See Current Flights"
        Query: public.searchFlights() is used to get past flights, then customer.makeRating() is used to insert the rating, which calls customer.getRatings()
            to make sure the customer has only one rating per flight
    
    See Spending: This button brings you to a page that displays your spending by month and total spending over the current year
    You can input a date range to see the tables and total spending over that range of time
        Query: public.getTickeDateRange is used to query for for total purchases within a time interval by joining buys and ticket  
    
    Logout: This will end your session.

Staff Home:
    Home Screen/Past and Current Flights: On the home screen a table for every flight your airline runs that will depart in within the next 30
    days will appear. To see flights beyond this, you can use the Departed _ Days Ago and Departs in _ Days forms to view flights
    further in the past or more in the future. You cannot view past and future flights at the same time
        Query: staff.getAirline() is used to get the airline by staff username, then public.searchFlights is used to query for flights. 
    
    Swap Status: When viewing future flights, you can click the "swap Status" button under Change Status to swap its status
        Query: displaying flights previously searched for, it can use the found primary key to query for the flight and change the status

    View Ratings: When viewing past flights, you can click the "View Ratings" to see the ratings and comments of that flight 
        Query: by using the previously obtained flight primary key from public.searchFlights(). staff.getAverageRating() is used to find the average rating

    View Customers: When viewing future or past flights, you can click the "View Customers" button to view every customer who has bought a 
    ticket for that flight 
        Query: staff.getCustomersByFlight() is used to select distinct customer emails and names when joining customer, ticket, and flight
            information is obtained previously using public.searchFlights() 

    Add Data: Clicking the "Add Data" button will bring you to the add data page, here you can add 4 types of data to the database
        Add Flight: Adds a flight 
            Query: staff.checkAirportType() checks if airport type matches, staff.getAirline() finds the airline by email, gets airline from email, staff.addFlight() inserts the flight and 
                will call staff.checkUnderMaintenance() to make sure the time does not overlap with a maintenance and staff.getAirplane() to make sure the airplane exists
                Finally, staff.addCreates() will add the creates relationship for the airline making the flight
        Add Airplane: Adds an airplane, then displays all airplanes the airline owns  
            Query: staff.getAirline() finds the airline by email, staff.addAirplane() inserts the airplane to the table, the runs staff.updateAirplaneManufacturing() to update airplane ages,
                finally it runs staff.getAllAirplane() to fetch every airplane the airline owns
        Add Airport: Adds an airport
            Query: staff.addAirport() inserts the airplort
        Add Maintenance: Adds a maintenance procedue to an airplane
            Query: staff.getAirline() finds the airline by email, staff.addMaintenance() will run checkMaintenanceConflictsWithFlight() to make sure the maintenance period does not overlap
                with a flight period, then it will insert into the maintenance table

    Search Flights: Will let you search for both future and past flights
        Query: it uses public.searchFlights() to find the flights 

    See Revenue: Will take you to the revenue page, which will display last month's earnings and last year's earnings. Additionally, 
    A table of every customer sorted by the amount of tickets they purchased, followed by the money that they spent
    over the last year. Clicking the "See Their Flights" button shows every distinct flight they bought a ticket for
        Query: staff.getAirline() finds the airline by email, public.getTickeDateRange is used to query for for total purchases within a time interval 
            by joining buys, ticket, flight, and creates. Then staff.getRevenue is used to get total money spent by customers in a time period by joining
            buys, ticket, flight, and creates