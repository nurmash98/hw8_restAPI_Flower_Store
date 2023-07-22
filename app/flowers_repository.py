from attrs import define
from pydantic import BaseModel
from app.database import * 
from sqlalchemy.orm import Session
from app.models import CreateFlower, UpdateFlower, CartResponse, ListCartResponse

class Flower(Base):
    __tablename__ = "flowers"
    flower_id = Column(Integer, primary_key = True)
    name = Column(String, index = True)
    count = Column(Integer)
    cost = Column(Integer)

class FlowersRepository:
    def get_all(self, db: Session):
        return db.query(Flower).all()
        
    def get_flower_by_id(self, db: Session, flower_id: int):
        return db.query(Flower).filter(Flower.flower_id == flower_id).first()

    def save(self, db: Session, flower: CreateFlower):
        db_flower = Flower(name = flower.name, count = flower.count, cost = flower.cost)
        db.add(db_flower)
        db.commit()
        db.refresh(db_flower)
        return db_flower.flower_id
    def update(self, db: Session, flower_id: int, flower: UpdateFlower):
        db.query(Flower).filter(Flower.flower_id == flower_id).update({Flower.name: flower.name, Flower.count: flower.count, Flower.cost: flower.cost})
        db.commit()
        return True
    
    def delete(self, db: Session, flower_id: int):
        db.query(Flower).filter(Flower.flower_id == flower_id).delete()
        db.commit()
        return flower_id
    
    def get_flowers_by_cart(self, db: Session, cart):
        db_flowers = db.query(Flower).filter(Flower.flower_id.in_(cart))
        flowers = []
        sum = 0
        for flower in db_flowers:
            new_flower = CartResponse(name = flower.name, count = flower.count, cost = flower.cost)
            sum += flower.count * flower.cost
            flowers.append(new_flower)
        return flowers, sum