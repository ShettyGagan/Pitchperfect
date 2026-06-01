from typing import Annotated
from datetime import datetime,timedelta, timezone

from fastapi import Depends,HTTPException,status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
import os
 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security_scheme=HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def hash_password(password:str)->str:
    return pwd_context.hash(password)

def verify_password(password:str,hashed_password:str)->bool:
    return pwd_context.verify(password,hashed_password)


def create_access_token(user_id:str,email:str)->str:
    payload={
        "sub":user_id,
        "email":email,
        "exp":datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }

    token=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return token


def get_current_user(credentials:Annotated[HTTPAuthorizationCredentials,Depends(security_scheme)])->dict:
    token =credentials.credentials
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id:str=payload.get("sub")
        email:str=payload.get("email")

        if user_id is None or email is None:
             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
        return{"user_id":user_id,"email":email}   
    except JWTError:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    