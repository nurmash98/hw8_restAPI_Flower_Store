from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Store(Base):
    __tablename__ = 'stores'
    store_id = Column(Integer, primary_key = True)
    name = Column(String)
    phone = Column(Text)
    city = Column(Text, nullable = False)



class Product(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key = True)
    name = Column(String)
    store_id = Column(ForeignKey("stores.store_id"))

    
