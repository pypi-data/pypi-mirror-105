from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sro_db.config.config import engine, session
from sro_db.model.core.models import ApplicationReference

class BaseService():
    
    def __init__(self, object):
        self.object = object
        self.type = self.object.__tablename__
   

    def __create_session_connection(self):
        Session = scoped_session(sessionmaker(bind=engine,autocommit=True))
        self.session = Session()
        self.session.begin(subtransactions=True)


    def find_all(self):
        self.__create_session_connection()
        results = self.session.query(self.object).order_by(self.object.id).all()
        return results

    def get_all(self):
        self.__create_session_connection()
        return self.session.query(self.object).order_by(self.object.id).all()
    
    def get_by_uuid(self, uuid):
        self.__create_session_connection()
        return self.session.query(self.object).filter(self.object.uuid == uuid).first()
        
    def create(self, object):        
        try:            
            self.__create_session_connection()
            local_object = self.session.merge(object)
            self.session.add(local_object)
            self.session.commit()            
            return local_object
        except:
            self.session.rollback() 
            raise

    def update(self, object):
        
        try:
            self.__create_session_connection()
            self.session.query(self.object).filter(self.object.id == object.id).update({column: getattr(object, column) for column in self.object.__table__.columns.keys()})
            self.session.commit()
        except:
            self.session.rollback() 
            raise

    def delete(self, object):
        self.__create_session_connection()
        try:
            self.session.delete(object)
            self.session.commit()
        except:
            self.session.rollback() 
            raise
