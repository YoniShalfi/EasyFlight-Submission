from flask_restful import Resource
from flask import request, session
from models import db
from facades import FacadeBase
from logger_config import logger



base_facade = FacadeBase(db_session=db.session)  


    


class CreateUserResource(Resource):
    def __init__(self, facade, base_facade):
        self.facade = facade
        self.base_facade = base_facade

    def post(self):
        """
        Create a new user by given username, password, email and user_role_id
        user_role_id is optional, default value is 2 (regular user)
        """

        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')  
        user_role_id = data.get('user_role_id', 2)


        try:
            user_dict = self.base_facade.create_new_user(username, password, email, user_role_id)
            logger.info(f'new user created: {user_dict["username"]}, please log in')
            return {'new user created: ': f'{user_dict["username"]}, please log in'}, 201
        except Exception as e:
            error_message = str(e)
            logger.error(f'error creating new user: {error_message}')
            return {'error': error_message}, 500  
