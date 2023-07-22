from attrs import define 
from pydantic import BaseModel

from app.database import *
from app.models import CreateUser
from sqlalchemy.orm import Session

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key = True, index = True)
    username = Column(String, index = True)
    email = Column(String, index = True)
    full_name = Column(String)
    password = Column(String)



class UsersRepository:
    def save(self, db: Session, user: CreateUser) -> User:
        db_user = User(email = user.email, username = user.username, full_name = user.full_name, password = user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    def getAll(self):
        print (self.users)
    
    def get_by_email(self, db: Session, email: str):
        db_user = db.query(User).filter(email == email).first()
        return db_user
    
    def get_by_username(self, db: Session,username: str):
        db_user = db.query(User).filter(username == username).first()
        return db_user


    def get_by_id(self, user_id):
        for user in self.users:
            if user.id == user_id:
                return user
        return None