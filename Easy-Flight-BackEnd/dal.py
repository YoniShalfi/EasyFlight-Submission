#dal.py
from models import( 
Country,
Customer,
User, Administrator,
AirlineCompany,
Ticket,
UserRole,
Flight)
from sqlalchemy.orm import aliased
from sqlalchemy.orm import joinedload



class DAL:
    """
    This class handles all the database operations.
    """

    def __init__(self, db_session):
        from models import db
        self.db_session = db.session

    def get_by_id_all(self, model, airline_company_id):
        """
        This method retrieves all instances of the given model based on the given id.
        """
        
        query = self.db_session.query(model)
        
        if model == Flight:
            query = (query
                    .options(joinedload(Flight.airline_company))
                    .options(joinedload(Flight.origin_country))
                    .options(joinedload(Flight.destination_country)))
        return query.filter_by(airline_company_id=airline_company_id).all()



    def get_by_id(self, model, id):
        """
        This method retrieves an instance of the given model based on the given id.
        """
        query = self.db_session.query(model)
        
        if model == Flight:
            query = (query
                    .options(joinedload(Flight.airline_company))
                    .options(joinedload(Flight.origin_country))
                    .options(joinedload(Flight.destination_country)))
        print(f' queried from dal: {query.filter_by(id=id).first()}')
        print(f'type from dal = {type(query.filter_by(id=id).first())}')
        return query.filter_by(id=id).first()
    



    def get_all(self, model):
        """
        This method retrieves all instances of the given model.
        """
        query = self.db_session.query(model)
        
        if model == Flight:
            query = (query
                    .options(joinedload(Flight.airline_company))
                    .options(joinedload(Flight.origin_country))
                    .options(joinedload(Flight.destination_country)))
            
        print(f' queried from dal: {query.all()}')
        return query.all()
    

    def add(self, instance):
        """
        This method adds an instance to the database.
        """
        self.db_session.add(instance)
        self.db_session.commit()

    def update(self):
        """
        This method updates an instance in the database.
        """
        self.db_session.commit()

    def add_all(self, instances):
        """
        This method adds multiple instances to the database.
        """
        self.db_session.add_all(instances)
        self.db_session.commit()

    def remove(self, instance):
        """
        This method removes an instance from the database.
        """
        self.db_session.delete(instance)
        self.db_session.commit()

    def get_customer_by_username(self, username):
        """
        This method retrieves a customer based on the given username.
        """
        user = User.query.filter_by(username=username).first()
        if user and user.customer:
            instance = user.customer
            print(f"from dal:  {instance}")
            return instance

        else:
            return None

    
    def get_by_parameters(self, model, **parameters):
        """
        This method retrieves an instance of the given model based on the given parameters.
        """
        origin_country_alias = aliased(Country)
        destination_country_alias = aliased(Country)

        query = self.db_session.query(model).join(
            AirlineCompany, model.airline_company_id == AirlineCompany.id
        ).join(
            origin_country_alias, model.origin_country_id == origin_country_alias.id
        ).join(
            destination_country_alias, model.destination_country_id == destination_country_alias.id
        )

        for key, value in parameters.items():
            query = query.filter(getattr(model, key) == value)

        query = query.options(
            joinedload(model.airline_company),
            joinedload(model.origin_country),
            joinedload(model.destination_country)
        )

        return query.all()


    def get_flights_by_customer(self, customer_id):
        """
        This method retrieves all flights of a customer based on the given customer id.
        """

        return self.db_session.query(Ticket).filter_by(customer_id=customer_id).all()
    
    def get_user_by_username(self, username):
        """
        This method retrieves a user based on the given username.
        """
        return User.query.filter_by(username=username).first()
    
    def get_ticket_by_booking_code(self, booking_code):
        """ 
        This method retrieves a ticket based on the given booking code.
        """
        return self.db_session.query(Ticket).filter_by(booking_code=booking_code).first()

