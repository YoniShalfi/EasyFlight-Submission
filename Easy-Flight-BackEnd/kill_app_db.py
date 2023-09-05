from models import  db 
from app import app
from logger_config import logger


def kill_db():
    '''
    this function drops the database
    it is used for testing purposes only and should not be used in production!
    '''
    db.drop_all()
    logger.critical('db killed')
    print('db killed')


# try:

#     with app.app_context():
#             kill_db()

# except Exception as e:
#     print(e)
#     logger.critical(f'error killing db: {e}')




