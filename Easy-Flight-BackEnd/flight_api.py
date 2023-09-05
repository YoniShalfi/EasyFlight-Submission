#flight_api.py
from flask_restful import Resource, marshal_with, fields, Api, marshal, reqparse
from facades import FacadeBase, AirlineFacade
from models import db
from flask import jsonify, request, session
from logger_config import logger



airline_company_fields = {
    'id': fields.Integer,
    'name': fields.String,
}

country_fields = {
    'id': fields.Integer,
    'name': fields.String,
}

flight_fields = {
    'id': fields.Integer,
    'airline_company': fields.Nested(airline_company_fields),
    'origin_country': fields.Nested(country_fields),
    'destination_country': fields.Nested(country_fields),
    'departure_time': fields.String(),
    'landing_time': fields.String(),
    'remaining_Tickets': fields.Integer,
}


facade = FacadeBase(db_session=db.session)  
facade_Airline_Facade = AirlineFacade(db_session=db.session)


class FlightResource(Resource):
    def __init__(self, facade, facade_Airline_Facade):
        self.facade = facade
        self.facade_Airline_Facade = facade_Airline_Facade
    

    @marshal_with(flight_fields)
    def get(self, flight_id=None):
        """
        Get all flights or a specific flight by id
        """
        if flight_id is not None:
            flight, status = self.facade.get_flight_by_id(flight_id)
            if status == 200:  
                print(f'quried from api: {flight}')
                logger.info(f'quried from api: {flight}')
                return flight
            
            logger.error(f'Flight not found')
            return {'error': 'Flight not found'}, 404
        
        else:
            flights, _ = self.facade.get_all_flights()  
            print(f'quried from api: {flights}')  
            logger.info(f'quried from api: {flights}')       
            return flights
        


    @marshal_with(flight_fields)
    def post(self):
        """
        Add a new flight
        it is possible to add a flight only if the user is an airline company or admin
        """
        try:

            data = request.get_json()
            departure_time = data['departure_time']
            landing_time = data['landing_time']
            origin_country_id = data['origin_country_id']
            destination_country_id = data['destination_country_id']
            remaining_tickets = data['remaining_tickets']
           
            user_role = request.headers.get('UserRole')
            airline_company_id = request.headers.get('UserID')
            
            if user_role != 'User' and user_role is not None:
                response, status_code = self.facade_Airline_Facade.add_flight(
                    airline_company_id=airline_company_id,
                    departure_time=departure_time,
                    landing_time=landing_time,
                    origin_country_id=origin_country_id,
                    destination_country_id=destination_country_id,
                    remaining_tickets=remaining_tickets
                )
                logger.info(f'Flight added successfully')
                return response, status_code
            else:
                response = {'error': 'Unauthorized access'}
                logger.error(f'Unauthorized access')
                return response, 403
                        
        except Exception as e:
            logger.error(f'error: {e}')
            print(f'error: {e}')
            return {'error': e}, 400

        
    # @marshal_with(flight_fields)
    # def post(self):
    #     """
    #     Add a new flight
    #     it is possible to add a flight only if the user is an airline company or admin
    #     """
    #     try:
    #         session_data = session.get('login_token')
    #         print (f'from adding flight session data : {session_data}')

    #         data = request.get_json()
    #         departure_time = data['departure_time']
    #         landing_time = data['landing_time']
    #         origin_country_id = data['origin_country_id']
    #         destination_country_id = data['destination_country_id']
    #         remaining_tickets = data['remaining_tickets']
           
    #         user_role = session_data.get('role')
    #         airline_company_id = session_data.get('air_line_company_id')
            
            
    #         if user_role != 'User' and user_role is not None:
    #             print(session)
    #             response, status_code = self.facade_Airline_Facade.add_flight(
    #                 airline_company_id=airline_company_id,
    #                 departure_time=departure_time,
    #                 landing_time=landing_time,
    #                 origin_country_id=origin_country_id,
    #                 destination_country_id=destination_country_id,
    #                 remaining_tickets=remaining_tickets
    #             )
    #             logger.info(f'Flight added successfully')
    #             return response, status_code
    #         else:
    #             response = {'error': 'Unauthorized access'}
    #             logger.error(f'Unauthorized access')
    #             return response, 403
                        
    #     except Exception as e:
    #         logger.error(f'error: {e}')
    #         print(f'error: {e}')
    #         return {'error': e}, 400
        

    @marshal_with(flight_fields)
    def put(self, flight_id):
        """
        Update a flight
        """

        try:
            data = request.get_json()
            response, status_code = self.facade_Airline_Facade.update_flight(flight_id, data)
            return response, status_code
        except Exception as e:
            print(e)
            return {'error': 'Invalid request'}, 400 
    


    @marshal_with(flight_fields)
    def delete(self, flight_id):
        """
        Delete a flight
        """

        try:
            print("Starting delete operation...")
            
            response, status_code = self.facade_Airline_Facade.remove_flight(flight_id)
            
            print("Deletion response:", response)
            print("Deletion status code:", status_code)
            logger.info(f'Flight deleted successfully') 
            return response, status_code

        except Exception as e:
            print("Exception:", e)
            logger.error(f'error: {e}')
            return {'error': 'Invalid request'}, 400



flightParams_fields = {
    'id': fields.Integer,
    'airline_company': fields.Nested(airline_company_fields),
    'origin_country': fields.Nested(country_fields),
    'destination_country': fields.Nested(country_fields),
    'departure_time': fields.DateTime(dt_format='iso8601'),
    'landing_time': fields.DateTime(dt_format='iso8601'),
    'remaining_Tickets': fields.Integer,
}

class FlightByParamsResource(Resource):
    def __init__(self, **kwargs):
        self.facade = kwargs.get('facade')
        self.facade_Airline_Facade = kwargs.get('facade_Airline_Facade')

    def get(self):
        """
        Get flights by parameters
        """
        try:
            parameters = request.args.to_dict()
            flights_data = self.facade.get_flights_by_parameters(flight_fields, **parameters)
            logger.info(f'quried from api: {flights_data}')
            return flights_data, 200
        
        except Exception as e:
            print("params", parameters)
            print(f'error :  {e}')
            logger.error(f'error: {e}')
            logger.error(f'error: {parameters}')
            return {'error': 'Invalid request'}, 400


class GetMyFlightsResource(Resource):
    def __init__(self, **kwargs):
        self.facade = kwargs.get('facade')
        self.facade_Airline_Facade = kwargs.get('facade_Airline_Facade')

    def get(self):
        """
        Get all flights of the logged in airline company
        """
        try:
            flights = self.facade_Airline_Facade.get_my_flights()

            if flights:
                logger.info(f'queried from api: {flights}')
                return [flight.to_dict() for flight in flights]
            else:
                return {"message": "No flights found"}, 404

        except Exception as e:
            logger.error(f'error: {str(e)}')
            return {'error': str(e)}, 500
            
