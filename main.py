from fastapi import FastAPI
from pydantic import BaseModel

app= FastAPI()


# #Home Route
# @app.get("/")
# def home():
#     return {"message": "Hello World"}


# @app.get("/about")
# def about():
#     return {"message": "This is the about page"}

# @app.get("/contact")
# def contact():
#     return {"message": "This is the contact page"}



# Path parameter + dynamic route + validation
# @app.get("/user/{user_id}")
# def get_user(user_id: int):
#     return {"user_id": user_id}


# Query Parameter +Optional Query Parameter


# @app.get("/users")
# def get_users(name: str=None, age: int=None):
#     return {"name": name, "age": age}


# @app.get("/products")
# def get_products(limit:int=10):
#     return {"limit": limit}


# Request Body + Post Api 

    
    
class Address(BaseModel):
    street: str
    city: str
    country: str
class User(BaseModel):
    name: str
    age: int
    email: str
    address: Address
    
@app.post("/create_user")
def create_user(user: User):
    return {
        "message": "User created successfully",
        "user": user}
