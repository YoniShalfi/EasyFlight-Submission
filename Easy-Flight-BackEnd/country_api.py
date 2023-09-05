from flask_restful import Resource, marshal_with, fields
from models import db
from facades import FacadeBase
from logger_config import logger


country_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'picture': fields.String,
}




class CountryResource(Resource):
    """
    This method retrieves country information based on the provided country_id. If no country_id is provided, it fetches information about all countries.
    """

    def __init__(self, facade, facade_Airline_Facade):
        self.facade = facade
        self.facade_Airline_Facade = facade_Airline_Facade

    def get(self, country_id=None):
        if country_id is not None:
            country, status = self.facade.get_country_by_id(country_id)
            if status == 200:  
                print(f'quried from api: {country}')
                logger.info(f'quried from api: {country}')
                return country
            return {'error': 'Flight not found'}, 404
        
        else:
            countries, _ = self.facade.get_all_countries()  
            print(f'quried from api: {countries}')  
            logger.info(f'quried from api: {countries}')       
            return countries
