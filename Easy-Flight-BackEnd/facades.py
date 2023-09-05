
#facades.py
from dal import DAL
from logger_config import logger
from flask import jsonify, session, json
from flask import request
from models import( db,
Country,Customer, User, Administrator,AirlineCompany,Ticket,UserRole,Flight)

from dal import DAL
from datetime import datetime
from  flask_restful import marshal
from sqlalchemy.orm import aliased
from datetime import datetime
from collections import OrderedDict
from sqlalchemy.orm import joinedload
from flask_cors import cross_origin

db_session = db.session
dal = DAL(db_session)


class LoginToken:
    """
        This class represents a login token.
        It is used to store the user's login information in the session.
    """
    def __init__(self, id, name, role, user, air_line_company_id=None, customer_id=None):
        self.id = id
        self.name = name
        self.role = role
        self.user = user
        self.air_line_company_id = air_line_company_id
        self.customer_id = customer_id

    def to_dict(self):
        """
        This method returns a dictionary representation of the login token.
        """
        return {
            'id': self.id,
            'name': self.name,
            'role': self.role,
            'user': self.user.id,
            'air_line_company_id': self.air_line_company_id,
            'customer_id': self.customer_id
        }


class FacadeBase:
    """
    This class is the base class for all facades.
    """

    def __init__(self, db_session):
        self.dal = DAL(db_session)

    def get_all_flights(self): 
        """
        This method retrieves all flights from the database using the DAL class.
        """ 
        try:
            flights = self.dal.get_all(Flight)
            logger.info('Fetched all flights')
            print(f'quried from facades : {[flight.to_dict() for flight in flights]}')
            return [flight.to_dict() for flight in flights], 200
        except Exception as e:
            logger.error('Error fetching flights: %s', e)
            return {'error': 'Error fetching flights'}, 500


    def get_flight_by_id(self, flight_id):
        """
        This method retrieves a flight based on the given flight_id using the DAL class.
        """

        try:
            flight = self.dal.get_by_id(Flight, flight_id)
            if flight:
                logger.info('Fetched flight with id %s', flight_id)
                print(f'quried from facades : {flight.to_dict()}')

                return flight.to_dict(), 200
            else:
                logger.info('Flight not found with id %s', flight_id)
                return {'error': 'Flight not found'}, 404
        except Exception as e:
            logger.error('Error fetching flight by id: %s', e)
            return {'error': 'Error fetching flight by id'}, 500



    def get_flights_by_parameters(self, flight_fields, **parameters):
        """
        This method retrieves flights based on the given parameters using the DAL class.
        """

        try:
            print("Received parameters:", parameters)

            if 'origin_country__name' in parameters:
                origin_country_name = parameters.pop('origin_country__name')
                origin_country = Country.query.filter_by(name=origin_country_name).first()
                if origin_country:
                    parameters['origin_country_id'] = origin_country.id

            if 'destination_country__name' in parameters:
                destination_country_name = parameters.pop('destination_country__name')
                destination_country = Country.query.filter_by(name=destination_country_name).first()
                if destination_country:
                    parameters['destination_country_id'] = destination_country.id

            if 'airline_company__name' in parameters:
                airline_company_name = parameters.pop('airline_company__name')
                airline_company = AirlineCompany.query.filter_by(name=airline_company_name).first()
                if airline_company:
                    parameters['airline_company_id'] = airline_company.id

            flights = self.dal.get_by_parameters(Flight, **parameters)
            
            logger.info('Fetched flights by parameters: %s', parameters)
            return [flight.to_dict() for flight in flights]

        except Exception as e:
            logger.error('Error fetching flights by parameters: %s', e)
            print("Exception:", e)
            return jsonify({'error': 'Invalid request'}), 400




    def get_all_airlines(self):
        """
        This method retrieves all airlines from the database using the DAL class.
        """
        try:
            airlines = self.dal.get_all(AirlineCompany)
            logger.info('Fetched all airlines')
            print(f'queried from facade: {[airline.to_dict() for airline in airlines]}')
            return jsonify([airline.to_dict() for airline in airlines]), 200
        
        except Exception as e:
            logger.error('Error fetching airlines: %s', e)
            return jsonify({'error': 'Error fetching airlines'}), 500

    def get_airline_by_id(self, id):
        """
        This method retrieves an airline based on the given id using the DAL class.
        """
        try:
            airline = self.dal.get_by_id(AirlineCompany, id)
            if airline:
                logger.info('Fetched airline with id %s', id)
                print(f'queried from facade:{airline.to_dict()}')
                logger.info('Fetched airline with id %s', id)
                return jsonify(airline.to_dict()), 200

            else:
                logger.info('Airline not found with id %s', id)
                return jsonify({'error': 'Airline not found'}), 404
            
        except Exception as e:
            logger.error('Error fetching airline by id: %s', e)
            return jsonify({'error': 'Error fetching airline by id'}), 500
        
    def get_airline_by_name(self, name):
        """
        This method retrieves an airline based on the given name using the DAL class.
        """
        try:
            airline = self.dal.get_airline_by_name(name)
            if airline:
                logger.info('Fetched airline with name %s', name)
                return jsonify(airline.to_dict()), 200
            else:
                logger.info('Airline not found with name %s', name)
                return jsonify({'error': 'Airline not found'}), 404
        except Exception as e:
            logger.error('Error fetching airline by name: %s', e)
            return jsonify({'error': 'Error fetching airline by name'}), 500


    def get_all_countries(self):
            """
            This method retrieves all countries from the database using the DAL class.
            """

            try:
                countries = self.dal.get_all(Country)
                logger.info('Fetched all countries')
                return jsonify([country.to_dict() for country in countries]), 200
            except Exception as e:
                logger.error('Error fetching countries: %s', e)
                return jsonify( {'error': 'Error fetching countries'}), 500
            
    def get_country_by_id(self, id):
        """
        This method retrieves a country based on the given id using the DAL class.
        """
        try:
            country = self.dal.get_by_id(Country, id)
            if country:
                logger.info('Fetched country with id %s', id)
                return jsonify(country.to_dict()), 200
            else:
                return jsonify({'error': 'Country not found'}), 404
        except Exception as e:
            logger.error('Error fetching country by id: %s', e)
            return jsonify({'error': 'Error fetching country by id'}), 500
        

    def create_new_user(self, username, password, email, user_role_id=2 ):
        """
        This method creates a new user using the DAL class.
        user role id 2 is for customer as default.
        """

        try:
            user = User(username=username, email=email, user_role_id=user_role_id)
            user.set_password(password)
            self.dal.add(user)
            self.dal.update()
            logger.info('Created new user %s', user)
            return user.to_dict()  
        
        except Exception as e:
            logger.error('Error creating new user: %s', e)
            return {'error': 'Error creating new user'}
        

    def create_new_user_with_customer(self, username, password, email):
        """
        This method creates a new user if customer not exist before.
        """

        try:
            user = User(username=username, email=email)
            user.set_password(password)
            self.dal.add(user)
            self.dal.update()
            logger.info('Created new user %s', user)
            return user
        
        except Exception as e:
            logger.error('Error creating new user: %s', e)
            return {'error': 'Error creating new user'}

class AnonymousFacade(FacadeBase):
    def __init__(self, db_session, login_token=None):
        super().__init__(db_session)
        self._login_token = login_token

    @property
    def login_token(self):
        return self._login_token

    def login(self, username, password):
        """
        This method logs in a user based on the given username and password.
        """
        user = self.dal.get_user_by_username(username)

        if user and user.check_password(password):
            role = user.user_role_relationship.role_name
            air_line_company_id = None
            customer_id = None

            customer_id = user.customer_relationship.id if user.customer_relationship else None

            if role == 'Air Line Company' and user.airline_company_relationship:
                air_line_company_id = user.airline_company_relationship[0].id if user.airline_company_relationship else None
            
            #create login token based on role + air_line_company_id and customer_id if exist
            login_token = LoginToken(
                id=user.id, 
                name=user.username, 
                role=role, 
                user=user, 
                air_line_company_id=air_line_company_id,
                customer_id=customer_id
            )

            print(f"LoginToken created: {login_token.to_dict()}") 
            logger.info('User logged in: %s', user)
            token_dict = login_token.to_dict()
            
            session['login_token'] = token_dict
            print(f'session = {session}')

            #  facade return based on role
            if role == 'User':
                return CustomerFacade(self.dal, login_token)
            elif role == 'Air Line Company':
                return AirlineFacade(self.dal, login_token)
            elif role == 'Administrator':
                return AdministratorFacade(self.dal, login_token)
            else:
                raise ValueError(f"Unexpected role: {role}")

        else:
            raise ValueError("Invalid credentials")

    @cross_origin()
    def logout(id, login_token):
        """
        This method logs out a user
        by removing the login token from the session.
        """            
        if login_token:
            session.pop('login_token')
            return {'message': 'User logged out'}, 200

        else:
            return {'error': 'No user is currently logged in'}, 400

    # @cross_origin()
    # def logout(id, token):
    #     """
    #     This method logs out a user
    #     by removing the login token from the session.
    #     """            
    #     if token:
    #         print(f'{token} before pop')
    #         print(f'session = {session}')
    #         session.pop('login_token')
    #         print(f'{token} after pop')
    #         return {'message': 'User logged out'}, 200

    #     else:
    #         print(f'{token} not found - logiout()' )
    #         return {'error': 'No user is currently logged in'}, 400


    def add_customer(self, first_name, last_name, address, phone_no, credit_card_num, username, password, email):
        """
        This method adds a new customer to the database using the DAL class.
        if user exist, it will add customer to the user.
        if user not exist, it will create new user and add customer.
        """

        try:
            print("Inside add_customer - Before get_user_by_username")
            user = self.dal.get_user_by_username(username)
            print("User retrieved:", user)
            
            if not user:
                print("Creating new user...")
                user = self.create_new_user_with_customer(username, password, email)
                self.dal.add(user)  
                self.dal.update()
                logger.info('Created new user %s', user)


            print("Creating customer...")

            customer = Customer(first_name=first_name, last_name=last_name, address=address, phone_no=phone_no,
                                credit_card_no=None, user=user)
            customer.credit_card_no =customer.hash_credit_card(credit_card_num) #hash credit card and update customer instance



            print(f'customer data : {customer}')
            self.dal.add(customer)
            logger.info('Customer added: %s', customer)
            return customer.to_dict()
        
        except Exception as e:
            logger.error('Error adding customer: %s', e)
            return {'error': 'Error adding customer'}, 500



class CustomerFacade(AnonymousFacade):
    
    def to_dict(self):
        return {
            'user_id': self.login_token.id,
            'username': self.login_token.name,
            'role': self.login_token.role
        }


    def update_customer(self, user_name, data):
        """
        This method updates a customer based on the given username and data using the DAL class.
        """
        try:
            user = self.dal.get_user_by_username(user_name)
            if user and user.customer:
                customers = user.customer  

                for customer in customers:
                    if 'first_name' in data:
                        customer.first_name = data['first_name']
                    if 'last_name' in data:
                        customer.last_name = data['last_name']
                    if 'address' in data:
                        customer.address = data['address']
                    if 'phone_no' in data:
                        customer.phone_no = data['phone_no']
                    if 'credit_card_no' in data:
                        hashed_credit_card = customer.hash_credit_card(data['credit_card_no'])
                        customer.credit_card_no = hashed_credit_card

                self.dal.update()
                logger.info('Customers updated successfully')
                return customers, 200
            else:
                return {'error': 'User not found or has no associated customer record'}, 404

        except ValueError as e:
            logger.error('Customers update failed: %s', e)
            return {'error': 'Customers update failed'}, 403


    # def add_ticket(self, flight_id, credit_card, tickets_number=1):
    #     """
    #     This method adds a new ticket to the database using the DAL class.
    #     it will check if the credit card is valid and if there is enough tickets.
    #     user must be logged in to add (buy) ticket.
    #     """
    #     try:
    #         flight = self.dal.get_by_id(Flight, flight_id)

    #         login_token = session.get('login_token')
    #         if login_token is None:
    #             raise ValueError("User not logged in or session expired.")
            
    #         customer_id = login_token.get('customer_id')
    #         if not customer_id:
    #             raise ValueError("No customer ID found in session.")
            

    #         customer = self.dal.get_by_id(Customer, customer_id)
    #         db_credit_card = customer.credit_card_no
    #         is_valid_card =  customer.check_credit_card(credit_card)
          
    #         if not is_valid_card:
    #             raise ValueError("The provided credit card is invalid.")


    #         if flight.remaining_Tickets >= tickets_number:
    #             booking_code = Ticket.generate_unique_booking_code()  
    #             ticket = Ticket(
    #                 flight_id=flight_id,
    #                 customer_id=customer_id,
    #                 tickets_number=tickets_number,
    #                 booking_code=booking_code)
                
              
    #             self.dal.add(ticket)
    #             flight.remaining_Tickets -= tickets_number  
    #             self.dal.update()
    #             logger.info('Ticket added successfully')
    #             return ticket.to_dict()
    #         else:
    #             raise ValueError("Not enough remaining tickets")
                
    #     except ValueError as e:
    #         logger.error('Ticket add failed: %s', e)
    #         return {'error': 'Ticket add failed'}, 400
                    

    def add_ticket(self, flight_id, credit_card, tickets_number=1):
        """
        This method adds a new ticket to the database using the DAL class.
        it will check if the credit card is valid and if there is enough tickets.
        user must be logged in to add (buy) ticket.
        """
        try:
            flight = self.dal.get_by_id(Flight, flight_id)

            customer_id = request.headers.get('UserID')
            print(f'from facade customer_id = {customer_id}')
            if not customer_id:
                raise ValueError("No customer ID found in session.")
            

            customer = self.dal.get_by_id(Customer, customer_id)
            db_credit_card = customer.credit_card_no
            is_valid_card =  customer.check_credit_card(credit_card)
          
            if not is_valid_card:
                raise ValueError("The provided credit card is invalid.")


            if int(flight.remaining_Tickets) >= int(tickets_number):
                booking_code = Ticket.generate_unique_booking_code()  
                ticket = Ticket(
                    flight_id=flight_id,
                    customer_id=customer_id,
                    tickets_number=tickets_number,
                    booking_code=booking_code)
                
              
                self.dal.add(ticket)
                flight.remaining_Tickets -= int(tickets_number)  
                self.dal.update()
                logger.info('Ticket added successfully')
                return ticket.to_dict()
            else:
                raise ValueError("Not enough remaining tickets")
                
        except ValueError as e:
            logger.error('Ticket add failed: %s', e)
            return {'error': 'Ticket add failed'}, 400

    # def get_my_tickets(self):
    #     """
    #     This method retrieves all tickets for the logged in customer using the DAL class.
    #     """
    #     try:
    #         login_token = session.get('login_token')
    #         customer_id = login_token['customer_id']
    #         tickets = self.dal.get_flights_by_customer(customer_id)

    #         logger.info('Fetched tickets for customer :%s', customer_id)
    #         return [ticket.to_dict() for ticket in tickets], 200
        
    #     except Exception as e:
    #         logger.error('Error fetching tickets: %s', e)
    #         return jsonify({'error': 'Error fetching tickets'}), 500
        
    def get_my_tickets(self):
        """
        This method retrieves all tickets for the logged in customer using the DAL class.
        """
        try:
            customer_id = request.headers.get('UserID')
            tickets = self.dal.get_flights_by_customer(customer_id)

            logger.info('Fetched tickets for customer :%s', customer_id)
            return [ticket.to_dict() for ticket in tickets], 200
        
        except Exception as e:
            logger.error('Error fetching tickets: %s', e)
            return jsonify({'error': 'Error fetching tickets'}), 500
        


    def remove_ticket(self, booking_code):
        """
        This method removes a ticket based on the given booking code using the DAL class.
        it is for customer to cancel his booking using booking code.
        """
        try:
            ticket = self.dal.get_ticket_by_booking_code(booking_code)
            
            if not ticket:
                raise ValueError(f"No ticket found with booking code: {booking_code}")

            self.dal.remove(ticket)

            flight = self.dal.get_by_id(Flight, ticket.flight_id)
            flight.remaining_Tickets += ticket.tickets_number
            self.dal.update()

            logger.info(f'Ticket with booking code {booking_code} removed successfully')
            return {'message': 'Ticket removed successfully'}, 200

        except ValueError as e:
            logger.error('Error removing ticket: %s', e)
            return {'error': str(e)}, 400
        
        except Exception as e:
            logger.error('Unexpected error removing ticket: %s', e)
            return {'error': 'Unexpected error while removing ticket'}, 500



class AirlineFacade(AnonymousFacade):

    def to_dict(self):
        return {
            'id': self._login_token.id,
            'username': self._login_token.name,
            'role': self._login_token.role
        }

    
    def get_my_flights(self):
        """
        This method retrieves all flights for the logged in airline using the DAL class.
        """
        model = Flight            
        user_role = request.headers.get('UserRole')
        id = request.headers.get('UserID')
            
        if not user_role or user_role != 'Air Line Company':
            logger.error("Unauthorized: Role mismatch or no role provided")
            return ("Unauthorized: Role mismatch or no role provided")

        try:
            print(f'from facade id = {id} | user_role = {user_role}')
            flights = self.dal.get_by_id_all(model=model, airline_company_id=id)
            logger.info(f'Fetched flights for airline id: {id}')
            return flights
        except Exception as e:
            logger.error(f'Error fetching flights: {str(e)}')
            return None
        

            # def get_my_flights(self):
    #     """
    #     This method retrieves all flights for the logged in airline using the DAL class.
    #     """
    #     model = Flight
    #     session_data = session.get('login_token')
    #     id = session_data.get('air_line_company_id')

    #     try:
    #         flights = self.dal.get_by_id_all(model=model, id=id)
    #         logger.info('Fetched flights for airline id: %s', id)
    #         return flights
    #     except Exception as e:
    #         logger.error('Error fetching flights: %s', e)
    #         return jsonify({'error': 'Error fetching flights'}), 500



    def update_airline(self, name):
        """
        This method updates an airline based on the given name using the DAL class.
        """
        try:
            session_data = session.get('login_token')
            id = session_data.get('air_line_company_id')

            company = self.dal.get_by_id(AirlineCompany, id) 

            if company:
                try:
                    company.name = name

                except Exception as e:
                    logger.error(e)
                    return('please provide an company data (name only)')

                self.dal.update()
                logger.info('Updated airline id: %s', id)
                return {'message': 'Airline updated'}, 200
            else:
                raise ValueError("Unauthorized")  
            
        except ValueError as e:
            logger.error('Error updating airline: %s', e)
            return jsonify({'error': 'Error updating airline'}), 400



    def add_flight(self, departure_time, landing_time, origin_country_id, destination_country_id, remaining_tickets, airline_company_id):
        """
        This method adds a new flight to the database using the DAL class.
        it will check if the departure time is before landing time and if origin country is not the same as destination country.
        it will check if the airline company id is the same as the logged in airline company id.
        """
        try:
            if departure_time > landing_time or origin_country_id == destination_country_id:
                raise ValueError("Invalid flight parameters")
            flight = Flight(departure_time=departure_time, landing_time=landing_time, origin_country_id=origin_country_id,
                            destination_country_id=destination_country_id, remaining_Tickets=remaining_tickets,
                            airline_company_id=airline_company_id)
            self.dal.add(flight)
            logger.info('Added flight with id: %s for airline id: %s', flight.id, airline_company_id)
            return jsonify(flight.to_dict()), 201
        except ValueError as e:
            logger.error('Error adding flight: %s', e)
            print(f'error from facade = {e}')
            return jsonify({'error': 'Error adding flight'}), 400



    def update_flight(self, flight_id, data):
        """
        This method updates a flight based on the given flight_id and data using the DAL class.
        it will check if the airline company id is the same as the logged in airline company id.
        """

        try:
            flight = self.dal.get_by_id(Flight, flight_id)
            if flight is None:
                return jsonify({'error': 'Flight not found'}), 404

            if 'login_token' not in session:
                print("Unauthorized: No login_token in session")
                logger.error('Unauthorized: No login_token in session')
                return jsonify({'error': 'Unauthorized access'}), 403

            login_token = session['login_token']
            print("login_token.id:", login_token.get('id'))
            print("flight.airline_company_id:", flight.airline_company_id)
            logger.info('login_token.id: %s', login_token.get('id'))

            if login_token.get('role') != 'Air Line Company':
                print("Unauthorized: ID mismatch")
                logger.error('Unauthorized: ID mismatch')
                return jsonify({'error': 'Unauthorized access'}), 403

            if 'departure_time' in data:
                flight.departure_time = data['departure_time']
            if 'landing_time' in data:
                flight.landing_time = data['landing_time']
            if 'origin_country_id' in data:
                flight.origin_country_id = data['origin_country_id']
            if 'destination_country_id' in data:
                flight.destination_country_id = data['destination_country_id']
            if 'remaining_tickets' in data:
                flight.remaining_Tickets = data['remaining_tickets']

            self.dal.update()
            logger.info('Updated flight id: %s', flight.id)
            return jsonify(flight.to_dict()), 200

        except ValueError as e:
            logger.error('Error updating flight: %s', e)
            return jsonify({'error': 'Error updating flight'}), 400





    def remove_flight(self, flight_id):
        """
        This method removes a flight based on the given flight_id using the DAL class.
        it will check if User role logged in or no one logged in and deny access.
        """
        try:
            flight = self.dal.get_by_id(Flight, flight_id)
            if flight is None:
                logger.error('Flight not found')
                return jsonify({'error': 'Flight not found'}), 404

            if 'login_token' not in session:
                logger.error('Unauthorized: No login_token in session')
                return jsonify({'error': 'Unauthorized access'}), 403

            login_token = session['login_token']
            if login_token.get('role') == 'User':
                logger.error('Unauthorized: Role mismatch')
                return jsonify({'error': 'Unauthorized access'}), 403

            self.dal.remove(flight)
            logger.info('Removed flight id: %s', flight_id)
            return jsonify({'message': 'Flight removed'}), 200

        except Exception as e:
            logger.error('Error removing flight: %s', e)
            return jsonify({'error': 'Error removing flight'}), 400




class AdministratorFacade(AnonymousFacade):
    

    def __init__(self, dal, login_token=None):
        super().__init__(dal)
        self._login_token = login_token

    def to_dict(self):
        return {
            'id': self._login_token.id,
            'username': self._login_token.name,
            'role': self._login_token.role
        }
    
    
    # def get_all_customers(self):
    #     """
    #     This method retrieves all customers from the database using the DAL class.
    #     it will check if the user role is Administrator and if so, it will return all customers.
    #     """
    #     try:
    #         if 'login_token' not in session:
    #             print("Unauthorized: No login_token in session")
    #             logger.error('Unauthorized: No login_token in session')
    #             return jsonify({'error': 'Unauthorized access'}), 403

    #         login_token = session['login_token']
    #         print("login_token.role:", login_token.get('role'))

    #         if login_token.get('role') != 'Administrator':
    #             print("Unauthorized: Role mismatch")
    #             return jsonify({'error': 'Unauthorized access'}), 403

    #         customers = self.dal.get_all(Customer)
    #         logger.info('Fetched all customers')
    #         return jsonify([customer.to_dict() for customer in customers]), 200
    #     except Exception as e:
    #         logger.error('Error fetching customers: %s', e)
    #         return jsonify({'error': 'Error fetching customers'}), 500


    def get_all_customers(self):
        """
        This method retrieves all customers from the database using the DAL class.
        It will check if the user role is Administrator and if so, it will return all customers.
        """
        try:
            
            user_role = request.headers.get('UserRole')
            
            if not user_role or user_role != 'Administrator':
                print("Unauthorized: Role mismatch or no role provided")
                return jsonify({'error': 'Unauthorized access'}), 403

            customers = self.dal.get_all(Customer)
            logger.info('Fetched all customers')
            return jsonify([customer.to_dict() for customer in customers]), 200
        except Exception as e:
            logger.error('Error fetching customers: %s', e)
            return jsonify({'error': 'Error fetching customers'}), 500



    # def get_customer_by_id(self, id):
    #     """
    #     This method retrieves a customer based on the given id using the DAL class.
    #     it will check if the user role is Administrator and if so, it will return the customer.
    #     """
    #     try:
    #         if 'login_token' not in session:
    #             print("Unauthorized: No login_token in session")
    #             logger.error('Unauthorized: No login_token in session')
    #             return jsonify({'error': 'Unauthorized access'}), 403

    #         login_token = session['login_token']
    #         print("login_token.role:", login_token.get('role'))
    #         logger.info('login_token.role: %s', login_token.get('role'))

    #         if login_token.get('role') != 'Administrator':
    #             print("Unauthorized: Role mismatch")
    #             logger.error('Unauthorized: Role mismatch')
    #             return jsonify({'error': 'Unauthorized access'}), 403

    #         customer = self.dal.get_by_id(Customer, id)
    #         if customer:
    #             logger.info('Fetched Customer with id %s', id)
    #             print(f'queried from facade: {customer.to_dict()}')
    #             return jsonify(customer.to_dict()), 200
    #         else:
    #             logger.info('Customer not found with id %s', id)
    #             return jsonify({'error': 'Customer not found'}), 404
            
    #     except Exception as e:
    #         logger.error('Error fetching Customer by id: %s', e)
    #         return jsonify({'error': 'Error fetching Customer by id'}), 500
            

    def get_customer_by_id(self, id):
        """
        This method retrieves a customer based on the given id using the DAL class.
        it will check if the user role is Administrator and if so, it will return the customer.
        """
        try:
            user_role = request.headers.get('UserRole')
            
            if not user_role:
                print("Unauthorized: No UserRole in headers")
                logger.error('Unauthorized: No UserRole in headers')
                return jsonify({'error': 'Unauthorized access'}), 403
            
            if user_role != 'Administrator':
                print("Unauthorized: Role mismatch")
                logger.error('Unauthorized: Role mismatch')
                return jsonify({'error': 'Unauthorized access'}), 403

            customer = self.dal.get_by_id(Customer, id)
            if customer:
                logger.info('Fetched Customer with id %s', id)
                return jsonify(customer.to_dict()), 200
            else:
                logger.info('Customer not found with id %s', id)
                return jsonify({'error': 'Customer not found'}), 404
            
        except Exception as e:
            logger.error('Error fetching Customer by id: %s', e)
            return jsonify({'error': 'Error fetching Customer by id'}), 500


    def add_airline(self, name, country_id):
            """
            This method adds a new airline to the database using the DAL class. 
            """
            try:
                airline = AirlineCompany(name=name, country_id=country_id)
                self.dal.add(airline)
                logger.info('Added new airline: %s', name)
                return jsonify(airline.to_dict()), 201
            except Exception as e:
                logger.error('Error adding airline: %s', e)
                return jsonify({'error': 'Error adding airline'}), 500
            
    def remove_airline(self, airline_id):
        """
        This method removes an airline based on the given airline_id using the DAL class.
        """

        if not airline_id:
            logger.error('Airline ID is required')
            return {'error': 'Airline ID is required'}, 400 
        
        try:
            airline = self.dal.get_by_id(AirlineCompany, airline_id)
            if airline:
                self.dal.remove(airline)
                logger.info('Removed airline with id: %s', airline_id)
                return jsonify({'success': 'Airline removed'}), 200
            else:
                return jsonify({'error': 'Airline not found'}), 404
        except Exception as e:
            logger.error('Error removing airline: %s', e)
            return jsonify({'error': 'Error removing airline'}), 500


    # def remove_customer(self, customer_id):
    #     """
    #     This method removes a customer based on the given customer_id using the DAL class.
    #     """

    #     try:
    #         customer = self.dal.get_by_id(Customer, customer_id)
    #         if customer:
    #             self.dal.remove(customer)
    #             logger.info('Removed customer with id: %s', customer_id)
    #             return {'success': 'Customer removed'}, 200
    #         else:
    #             logger.info('Customer not found with id %s', customer_id)   
    #             return {'error': 'Customer not found'}, 404
    #     except Exception as e:
    #         logger.error('Error removing customer: %s', e)
    #         return {'error': 'Error removing customer'}, 500
            


    def remove_customer(self, customer_id):
        """
        This method removes a customer based on the given customer_id using the DAL class.
        """
        try:
            user_role = request.headers.get('UserRole')

            if not user_role:
                logger.error('Unauthorized: No user data provided')
                return {'error': 'Unauthorized access'}, 403

         
            if user_role != 'Administrator':
                logger.error('Unauthorized: Role mismatch')
                return {'error': 'Unauthorized access'}, 403

            customer = self.dal.get_by_id(Customer, customer_id)
            if customer:
                self.dal.remove(customer)
                logger.info('Removed customer with id: %s', customer_id)
                return {'success': 'Customer removed'}, 200
            else:
                logger.info('Customer not found with id %s', customer_id)   
                return {'error': 'Customer not found'}, 404
            
        except Exception as e:
            logger.error('Error removing customer: %s', e)
            return {'error': f"Error removing customer: {str(e)}"}, 500


    def update_airline(self, airline_id, name=None, country_id=None):
        '''
        This method updates an airline based on the given airline_id using the DAL class.
        '''
        try:
            airline = self.dal.get_by_id(AirlineCompany, airline_id)
            if not airline:
                logger.error('Airline not found')
                return {'error': 'Airline not found'}, 404

            if name:
                airline.name = name
            if country_id:
                airline.country_id = country_id

            self.dal.update() 

            logger.info('Updated airline ID %d: %s', airline_id, name)
            return airline.to_dict()
        except Exception as e:
            logger.error('Error updating airline ID %d: %s', airline_id, e)
            return jsonify ({'error' : e})









