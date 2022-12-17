from jose import JWTError, jwt
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from . import schemas, models as db_model

oauth2_scheme_customers = OAuth2PasswordBearer(tokenUrl="/api/v1/login/customers", scheme_name='Customer')
oauth2_scheme_artistans = OAuth2PasswordBearer(tokenUrl="/api/v1/login/artistans", scheme_name='Artistan')

SECRET_KEY = "a24a58ab7d8691b306d39d94470af6ad9075f704c2a34ba86776120132e68ee7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data:dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")
        type: str = payload.get("user_type")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id, type=type)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_customer(token:str = Depends(oauth2_scheme_customers)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Aunthenticate": "Bearer"})
    # you can decide not to return token_data but get the user profile using the user id
    token_data = verify_access_token(token, credentials_exception)
    if token_data.type != db_model.Customer.__tablename__:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"id ({token_data.id}) not a customer!")
    return token_data

def get_current_artistan(token:str = Depends(oauth2_scheme_artistans)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Aunthenticate": "Bearer"})
    # you can decide not to return token_data but get the user profile using the user id
    token_data = verify_access_token(token, credentials_exception)
    if token_data.type != db_model.Artistan.__tablename__:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"id ({token_data.id}) not an artistan!")
    return token_data


