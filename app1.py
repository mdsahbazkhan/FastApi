# from fastapi import FastAPI
# import asyncio

# app = FastAPI()

# @app.get("/")

# async def home():
#     print("Processing request...")
#     await asyncio.sleep(4)  # Simulate a long-running operation
#     return {"message": "Hello, World!"}



from fastapi import FastAPI,Header,HTTPException,Depends
from jose import jwt
from datetime import datetime, timedelta ,timezone

app = FastAPI()

SECRET_KEY="sahbazsecretkey"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30


# Create Token
def create_token(data:dict):
    to_encode=data.copy()
    expire= datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    token=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    
    return token



# Login Api

@app.post("/login")

def login(username:str,password:str):
    if username!="admin" or password!="1234":
        raise HTTPException(status_code=401,detail="Invalid username or password")
    token=create_token({"sub":username})
    return {"access_token":token}

# Token Verify

def token_verify(token:str=Header(None)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

# Protected Route
@app.get("/protected")
def protected_route(user:dict=Depends(token_verify)):
    return {"message": "Secure Data Accessed",
            "user":user}