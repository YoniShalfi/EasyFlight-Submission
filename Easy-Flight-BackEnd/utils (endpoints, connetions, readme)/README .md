# Flight Booking System API

**This project is a Flight Booking System API that allows users, airline companies, and administrators to interact with the system through different facades. The API is built using Flask and SQLAlchemy, and it provides various endpoints for different roles.**

## API Endpoints

### Facade Base

- **GET /flights:** Retrieve a list of all flights.
- **GET /flights/{flight_id}:** Retrieve information about a specific flight by its ID.
- **GET /flights/parameters:** Retrieve flights based on parameters like origin country, destination country, and airline company.
- **GET /airline:** Retrieve a list of all airline companies.
- **GET /airline/{airline_id}:** Retrieve information about a specific airline company by its ID.
- **GET /country:** Retrieve a list of all countries.
- **GET /country/{country_id}:** Retrieve information about a specific country by its ID.
- **POST /createUser:** Create a new user with username, password, and email.

### Anonymous Facade

- **POST /login:** Log in with a username and password.
- **POST /logout:** Log out the current user.
- **POST /customers:** Add a new customer with details including credit card information.

### Administrator Facade

- **GET /customers:** Retrieve a list of all customers.
- **GET /customers/{customer_id}:** Retrieve information about a specific customer by their ID.
- **POST /airline:** Add a new airline with a name and country ID.
- **DELETE /airline/{airline_id}:** Remove an airline by its ID.
- **DELETE /customers/{customer_id}:** Remove a customer (and associated user) by their ID.

### Customer Facade

- **PUT /customers:** Update customer information, including first name and credit card number.
- **POST /buy:** Add a new ticket for the customer by specifying flight ID, ticket number, and credit card information.
- **DELETE /buy:** Remove a ticket by providing the booking code.
- **GET /buy:** Retrieve the list of tickets associated with the logged-in customer.

### Airline Facade

- **PUT /airline:** Update airline information, including the name.
- **POST /flights:** Add a new flight by providing departure and landing times, origin and destination countries, remaining tickets, and airline company ID.
- **PUT /flights/{flight_id}:** Update flight information by providing various fields.
- **DELETE /flights/{flight_id}:** Remove a flight by its ID.
- **GET /flights/airline:** Retrieve a list of flights associated with the logged-in airline company.
