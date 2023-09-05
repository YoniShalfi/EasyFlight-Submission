from flask_restful import Resource, marshal_with, fields
from facades import FacadeBase, AdministratorFacade
from models import db
from flask import request
from flask import session
from logger_config import logger

airline_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'user_id': fields.Integer,
}

facade = FacadeBase(db_session=db.session)  
admin_facade =  AdministratorFacade(dal="dal", login_token='login_token')  



class AirlineResource(Resource):
    """
This class represents a resource for managing airline-related operations through an API.
    """

    def __init__(self, facade, facade_Airline_Facade, admin_facade):
        self.facade = facade
        self.facade_Airline_Facade = facade_Airline_Facade
        self.admin_facade = admin_facade

    def get(self, airline_id=None):
        """
        Retrieve airline information or a list of airlines.
        """

        if airline_id is not None:
            airline, status = self.facade.get_airline_by_id(airline_id)
            if status == 200:  
                print(f'quried from api: {airline}')
                logger.info(f'quried from api: {airline}')
                return airline
            return {'error': 'Flight not found'}, 404
        else:
            airlines, _ = self.facade.get_all_airlines()  
            print(f'quried from api: {airlines}')  
            logger.info(f'quried from api: {airlines}')       
            return airlines
        


    # def post(self):
    #     """
    #     Add a new airline
    #     If the user is authorized and the airline is added successfully
    #     """

    #     data = request.get_json()
    #     name = data.get('name')
    #     country_id = data.get('country_id')

    #     try:
    #         login_token = session['login_token']
    #         if login_token.get('role') != 'Administrator':
    #             logger.info(f'Unauthorized access')
    #             return {'error': 'Unauthorized access'}, 403

    #         response_content, status_code = self.admin_facade.add_airline(name, country_id)
    #         if status_code == 201:  
    #             logger.info(f'Airline added successfully')
    #             return response_content.json, 201
    #         else:
    #             logger.info(f'Airline not added')
    #             return response_content.json, status_code
    #     except Exception as e:
    #         error_message = str(e)
    #         logger.error(f'Airline not added')
    #         return {'error': error_message}, 500  

    def post(self):
        """
        Add a new airline
        If the user is authorized and the airline is added successfully
        """

        data = request.get_json()
        name = data.get('name')
        country_id = data.get('country_id')

        try:
            user_role = request.headers.get('UserRole')

            if user_role != 'Administrator':
                logger.info(f'Unauthorized access')
                return {'error': 'Unauthorized access'}, 403
            
            response_content, status_code = self.admin_facade.add_airline(name, country_id)
            if status_code == 201:  
                logger.info(f'Airline added successfully')
                return response_content, 201
            else:
                logger.info(f'Airline not added')
                return response_content.json, status_code
        except Exception as e:
            error_message = str(e)
            logger.error(f'Airline not added : {e}')
            return {'error': error_message}, 500  


    # def delete(self, airline_id=None):
    #     """
    #     Delete an airline user is authorized and the airline is added successfully
    #     """
    #     airline_id = request.view_args.get('airline_id')
    #     print(f'api says that airline_id is {airline_id}')

    #     if not airline_id:
    #         logger.info(f'Airline ID is required')
    #         return {'error': 'Airline ID is required'}, 400  
        
        

    #     try:
    #         login_token = session['login_token']
    #         if login_token.get('role') != 'Administrator' or not login_token:
    #                 logger.info(f'Unauthorized access')
    #                 return {'error': 'Unauthorized access'}, 403

    #         response_content, status_code = self.admin_facade.remove_airline(airline_id)
    #         logger.info(f'Airline deleted successfully')    
    #         return response_content.json, status_code
        
    #     except Exception as e:
    #         error_message = str(e)
    #         logger.error(f'Airline not deleted: {e}')
    #         return {'error': error_message}, 500  
        

    def delete(self, airline_id=None):
        """
        Delete an airline user is authorized and the airline is added successfully
        """
        user_role = request.headers.get('UserRole')
        print(f'user_role header  = {user_role}')

        if user_role != 'Administrator':
            logger.info(f'Unauthorized access')
            return {'error': 'Unauthorized access'}, 403

        if not airline_id:
            logger.info(f'Airline ID is required')
            return {'error': 'Airline ID is required'}, 400  
        
        

        try:
            response_content, status_code = self.admin_facade.remove_airline(airline_id)
            logger.info(f'Airline deleted successfully')    
            return response_content.json, status_code
        
        except Exception as e:
            error_message = str(e)
            logger.error(f'Airline not deleted: {e}')
            return {'error': error_message}, 500  




    def put(self):
        """
        Update an airline user is authorized and the airline is added successfully
        """

        data = request.get_json()
        name = data.get('name')

        try:
            updated_airline_dict = self.facade_Airline_Facade.update_airline(name)
            logger.info(f'Airline updated successfully')
            return {'updated airline': updated_airline_dict}, 200
        
        except Exception as e:
            error_message = str(e)
            logger.error(f'Airline not updated: {e}')
            return {'error': error_message}, 500  
