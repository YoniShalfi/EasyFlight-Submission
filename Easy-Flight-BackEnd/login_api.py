#login_api.py
from flask_restful import Resource
from flask import request, session, jsonify
from models import db
from facades import AnonymousFacade, LoginToken, FacadeBase
from logger_config import logger



anonymous_facade = FacadeBase(db_session=db.session)  


class LoginResource(Resource):
    def __init__(self, facade, anonymous_facade):
        self.facade =  facade
        self.anonymous_facade = anonymous_facade


    def post(self):
        """
        Login a user by given username and password
        """
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        try:
            self.anonymous_facade.login(username, password)
            logger.info(f'User {username} logged in')
            return  jsonify(session['login_token'], 200  )
        
        except ValueError:
            logger.error(f'Invalid username or password')
            return {'error': 'Invalid username or password'}, 401
        

    def get(self):
        """
        Get the current logged in user
        """

        print(f'session = {session}') 

        if 'login_token' in session:
            login_token_data = session['login_token']
            print(login_token_data)
            logger.info(f'User {login_token_data} is currently logged in')
            return login_token_data, 200
            
        else:
            logger.info(f'No user is currently logged in')
            return {'message': 'No user is currently logged in'}, 200




class LogoutResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            user_id = data.get('id')
            token = data.get('login_token')
            db_session = db.session

            if token:
                print(f'logout token user: {user_id}')
                return AnonymousFacade.logout(id=user_id, login_token=token)
            
            return('cant logout, no user singed-in'), 410
        except Exception as e:
            print(f'logout error: {e}')
            logger.error (e)
