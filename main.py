from fastapi import FastAPI

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



