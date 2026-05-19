from fastapi import FastAPI,status,HTTPException,Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse

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

    
    
# class Address(BaseModel):
#     street: str
#     city: str
#     country: str
# class User(BaseModel):
#     name: str
#     age: int
#     email: str
#     address: Address
    
# @app.post("/create_user")
# def create_user(user: User):
#     return {
#         "message": "User created successfully",
#         "user": user}


# Path + Query + Request Body

# users=[]

# class User(BaseModel):
#     id: int
#     name: str
#     age: int
#     email: str
    
# @app.post("/users")

# def create_user(user:User):
#     users.append(user)
#     return {
#         "message": "User created successfully",
#         "user": user
#         }
    
# @app.put("/users/{user_id}")
# def update_user(user_id:int,user:User,notify: bool=False):
#   for user in users:
#       if user.id==user_id:
#           users[user_id]=user
          
#           return{
#               "message": "User updated",
#               "notify": notify,
#               "user": user
#           }
#       return {"message": "User not found"}
   
   
#    Response Model 
# class User(BaseModel):
#     id: int
#     name: str
#     age: int
#     email: str
#     password: str
    
    
# class UserResponse(BaseModel):
#     id: int
#     name: str
#     email: str

# @app.get("/users", response_model=UserResponse)
# def get_user():
#     return {
#         "id": 1,
#         "name": "John Doe",
#         "email": "john.doe@example.com",
#         "password":"123456"
#     }


# Exception Handling + HTTPException + Global Error Handler


# @app.get("/users/{user_id}")
# def get_user(user_id: int):
#     if user_id !=1:
#         raise HTTPException(
#             status_code=404,
#             detail="User not found"
#         )
#     return {
#         "id": 1,
#         "name": "John Doe"
#     }


class UserNotFoundException(Exception):
    def __init__(self,name:str):
        self.name=name
        
@app.exception_handler(UserNotFoundException)
def user_not_found_exception_handler(request:Request, exc:UserNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"message": f"User '{exc.name}' not found"}
    )
    
@app.get("/users/{name}")
def get_user(name:str):
    if name!="John":
        raise UserNotFoundException(name)
    return {
        "name": name,
        "age": 30
    }