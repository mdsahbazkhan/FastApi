from fastapi import FastAPI
from db import engine

import models

models.Base.metadata.create_all(bind=engine)

app=FastAPI()
@app.get("/")
def home():
    return {"message": "Welcome to the Blog API!"}