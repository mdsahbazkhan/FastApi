from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# # from dotenv import load_dotenv
# # import os
# from config import settings

app= FastAPI()
# # load_dotenv()

# # Allowed Origins for CORS (Frontend URLs)

# # origins=os.getenv("ORIGINS")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.origins, # Allow requests from specified origins
#     allow_methods=["*"], # Allow all HTTP methods (GET, POST, etc.)
#     allow_headers=["*"], # Allow all headers
#     allow_credentials=True # Allow cookies and authentication headers
# )

# @app.get("/")
# def home():
#     return {"message": "CORS is enabled for the specified origin"}


# @app.get("/")
# def home():
#     return {
#         "message":"Welcome to the Home Page"
#     }
    
# @app.get("/add")
# def add(a: int, b: int):
#     return {
#         "result": a + b
#     }
    
# @app.get("/subtract")
# def subtract(a: int, b: int):
#     return {
#         "result": a - b
#     }


import requests

@app.get("/posts")

def get_posts():
    response = requests.get("https://jsonplaceholder.typicode.com/posts")
    return response.json()

@app.get("/posts/{post_id}")
def get_post(post_id: int):
    response = requests.get(f"https://jsonplaceholder.typicode.com/posts/{post_id}")
    return response.json()