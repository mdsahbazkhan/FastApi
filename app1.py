# from fastapi import FastAPI
# import asyncio

# app = FastAPI()

# @app.get("/")

# async def home():
#     print("Processing request...")
#     await asyncio.sleep(4)  # Simulate a long-running operation
#     return {"message": "Hello, World!"}



from fastapi import FastAPI,Header,HTTPException,Depends
from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from datetime import datetime, timedelta ,timezone
from passlib.context import CryptContext



app = FastAPI()

SECRET_KEY="sahbazsecretkey"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Password Hashing
pwd_context=CryptContext(schemes=["pbkdf2_sha256"])

# OauthSetup

oauth2_schema =OAuth2PasswordBearer(tokenUrl="login")

# Dummy User Database
fake_users_db={
    "admin":{
        "username":"admin",
        "hashed_password":pwd_context.hash("1234")
    }
}
# Hash Password
def hash_password(password:str):
    return pwd_context.hash(password)

# Verify Password
def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

# Create Token
def create_token(data:dict):
    to_encode=data.copy()
    expire= datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    token=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    
    return token



# Login Api(OAuth2)

@app.post("/login")

def login(form_data:OAuth2PasswordRequestForm=Depends()):
    user=fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password,user["hashed_password"]):
        raise HTTPException(status_code=401,detail="Invalid username or password")
    token=create_token({"sub":form_data.username})
    return {"access_token":token,"token_type":"bearer"}

# def login(username:str,password:str):
#     if username!="admin" or password!="1234":
#         raise HTTPException(status_code=401,detail="Invalid username or password")
#     token=create_token({"sub":username})
#     return {"access_token":token}

# Token Verify
def token_verify(token:str=Depends(oauth2_schema)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username=payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )
        return username
    except JWTError :
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

# def token_verify(token:str=Header(None)):
#     try:
#         payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
#         return payload
#     except:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid or expired token"
#         )

# # Protected Route
@app.get("/protected")
def protected_route(user:dict=Depends(token_verify)):
    return {"message": "Secure Data Accessed",
            "user":user}