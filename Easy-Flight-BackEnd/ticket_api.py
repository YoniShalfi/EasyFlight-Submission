from flask import request, jsonify, session
from flask_restful import Resource
from facades import CustomerFacade  
from logger_config import logger

class TicketResource(Resource):
    def __init__(self, **kwargs):
        self.customer_facade = kwargs.get('customer_facade')

    def post(self):
        """
        Add a new ticket to the current logged in user
        """

        try:
            data = request.get_json()
            flight_id = data.get('flight_id')
            tickets_number = data.get('tickets_number', 1)
            credit_card = data.get('credit_card')

            if not credit_card:
                logger.error(f'Credit card information is missing')
                return {'error': 'Credit card information is missing'}, 400


            response = self.customer_facade.add_ticket(flight_id, credit_card, tickets_number)
            logger.info(f'New ticket added to user ')
            return response
            
        except Exception as e:
            print(f'Error from API: {e}')
            logger.error(f'Error from API: {e}')
            return {'error': 'Invalid request'}, 400
        

    def get(self):
        """
        Get all tickets of the current logged in user
        """

        try:
            response_data, status_code = self.customer_facade.get_my_tickets()
            logger.info(f'User tickets fetched successfully')
            return response_data, status_code
        
        except Exception as e:
            print(f'Error from API: {e}')
            logger.error(f'Error from API: {e}')
            return {'error': 'Error fetching tickets'}, 500
        
        
    def delete(self):
        """
        Remove a ticket from the current logged in user
        """
        try:
            data = request.get_json()
            booking_code = data.get('booking_code')
            
            if not booking_code:
                logger.error(f'Booking code is required.')
                raise ValueError("Booking code is required.")
            
            response, status_code = self.customer_facade.remove_ticket(booking_code)
            logger.info(f'Ticket {booking_code} removed successfully')
            return response, status_code
            
        except ValueError as e:
            logger.error(f'Error from API: {e}')
            return {'error': str(e)}, 400
        
        except Exception as e:
            logger.error(f'Error from API: {e}')
            print(f'Error from API: {e}')
            return {'error': 'Unexpected error while removing ticket'}, 500

