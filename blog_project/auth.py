from dotenv import load_dotenv
import os
from jose import jwt,JWTError
from datetime import datetime,timedelta,timezone
from fastapi import HTTPException,Depends,Header
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

load_dotenv()

oauth2_schema =OAuth2PasswordBearer(tokenUrl="login")

# Token Create
secret_key = os.getenv("SECRET_KEY", "mysecretkey")
algorithm = os.getenv("ALGORITHM", "HS256")
def create_token(data:dict):
    to_encode=data.copy()
    expire= datetime.now(timezone.utc) + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)))
    to_encode.update({"exp":expire})
    
    token=jwt.encode(to_encode,secret_key,algorithm=algorithm)
    return token
    

# Token Verify

def verify_token(token:str=Depends(oauth2_schema)):
 try:
     payload=jwt.decode(token,secret_key,algorithms=[algorithm])
     return payload
 except JWTError:
     raise HTTPException(status_code=401, detail="Invalid token")
 
 