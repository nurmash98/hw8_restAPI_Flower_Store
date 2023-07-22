from attrs import define
from pydantic import BaseModel
from app.database import *
from sqlalchemy.orm import Session
from app.flowers_repository import Flower
class Purchase(Base):
    __tablename__ = "purchases"
    purchase_id = Column(Integer, primary_key = True)
    user_id = Column(ForeignKey("users.user_id"))
    flower_id = Column(ForeignKey("flowers.flower_id"))

class PurchasesRepository:
    purchases: list[Purchase]

    def __init__(self):
        self.purchases = []

    # необходимые методы сюда
    def save(self, db: Session, purchase: Purchase):
        db.add(purchase)
        db.commit()
        db.refresh(purchase)
        return purchase
    # конец решения

    def get_flowers(self, db: Session, user_id):
        # flowers_id = db.query(Purchase).filter(user_id == user_id)
        flowers = db.query(Flower).join(Purchase, Flower.flower_id == Purchase.flower_id).filter(user_id == user_id)
        return flowers
