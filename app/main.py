from fastapi import FastAPI, Response, Request, Depends, Form, HTTPException, Cookie
from pydantic import BaseModel
from jose import jwt
from typing import Annotated, List
from .flowers_repository import Flower, FlowersRepository
from .purchases_repository import Purchase, PurchasesRepository
from .users_repository import User, UsersRepository
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .database import SessionLocal, engine
from app.models import CreateUser, ProfileResponse
from app.models import CreateFlower, UpdateFlower, PurchaseResponse
import json


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_schema = OAuth2PasswordBearer(tokenUrl = "login")
flowers_repo = FlowersRepository()
purchases_repo = PurchasesRepository()
users_repo = UsersRepository()



def encode_jwt(username: str) -> str:
    body = {"username" : username}
    token = jwt.encode(body, "Nurmash", "HS256")
    return token

def decode_jwt(token: str) -> str:
    data = jwt.decode(token, "Nurmash", "HS256")
    return data['username']

@app.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        session = SessionLocal()
        username = form_data.username
        db_user = users_repo.get_by_username(session, username)
        if not db_user:
            raise HTTPException(status_code=400, detail="Username not found")
        password = form_data.password
        if not password == db_user.password:
            raise HTTPException(status_code=400, detail="Incorrect password")
        token = encode_jwt(username)
        return {"access_token": token, "token_type": "bearer"}
    finally:
        session.close()



@app.post("/signup")    
def signup(user: CreateUser):
    try:
        session = SessionLocal()
        
        db_user = users_repo.save(session, user)
        return db_user
    finally:
        session.close()

@app.get("/profile", response_model = ProfileResponse)
def get_profile(token: Annotated[str, Depends(oauth2_schema)]):
    try:
        session = SessionLocal()
        username = decode_jwt(token)
        user = users_repo.get_by_username(session, username)
        if not user:
            return HTTPException(status_code = 404, detail = "User not found")
        profile = ProfileResponse(username = user.username, email = user.email, full_name = user.full_name)
        return profile
    finally:
        session.close()

@app.get("/flowers")
def get_flowers(token: Annotated[str, Depends(oauth2_schema)]):
    try:
        session = SessionLocal()
        return flowers_repo.get_all(session)
    finally:
        session.close()


@app.post("/flowers")
def post_flowers(flower: CreateFlower, token: Annotated[str, Depends(oauth2_schema)]) -> int:
    try:
        session = SessionLocal()
        flower = Flower(name = flower.name, count = flower.count, cost = flower.cost)
        flower_id = flowers_repo.save(session, flower)
        return {"flower_id": flower_id}
    finally:
        session.close()

@app.patch("/flower/{flower_id}")
def update_flower(token: Annotated[str, Depends(oauth2_schema)], flower_id: int, flower: UpdateFlower):
    try:
        session = SessionLocal()
        isUpdated = flowers_repo.update(session, flower_id, flower)
        return isUpdated
    finally:
        session.close()

@app.delete("/flower/{flower_id}")
def delete_flower(token: Annotated[str, Depends(oauth2_schema)], flower_id: int):
    try:
        session = SessionLocal()
        return flowers_repo.delete(session, flower_id)
    finally:
        session.close()


@app.get("/cart/items")
def get_cart_items(cart: str = Cookie(default = "[]")):
    try:
        session = SessionLocal()
        cart_json = json.loads(cart)
        flowers, sum = flowers_repo.get_flowers_by_cart(session, cart_json)  
        if not flowers:
            return Response("Not Valid Cart")
        return {"Flowers in cart" : flowers, "Sum" : sum}
    finally:
        session.close()

@app.post("/cart/items")
def post_cart_item(response: Response, flower_id: int = Form(), cart: str = Cookie(default = "[]")):
    response = Response("Added Flower")
    cart_json = json.loads(cart)
    if flower_id not in cart_json:
        cart_json.append(flower_id)
    new_cart = json.dumps(cart_json)
    response.set_cookie(key = "cart", value = new_cart)
    return response

@app.get("/purchased")
def get_purchased(token: Annotated[str, Depends(oauth2_schema)]):
    try: 
        session = SessionLocal()
        username = decode_jwt(token)
        user = users_repo.get_by_username(session, username)
        user_id = user.user_id
        flowers = purchases_repo.get_flowers(session, user_id)
        res = []
        for flower in flowers:        
            res.append(PurchaseResponse(name = flower.name, sum = flower.count * flower.cost))
        return res
    finally:
        session.close()

        
@app.post("/purchased")
def post_purchase(token: Annotated[str, Depends(oauth2_schema)], cart: str = Cookie(default = "[]")):
    try:
        session = SessionLocal()
        carts = json.loads(cart)
        username = decode_jwt(token)
        user = users_repo.get_by_username(session, username)
        user_id = user.user_id
        for cart in carts:
            purchases_repo.save(session, Purchase(user_id = user_id, flower_id = int(cart)))
        return Response("Added to purchase")
    finally:
        session.close()













