from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash(password:str):
    return pwd_context.hash(password)

def verify(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)


from pydantic import BaseSettings

class Settings(BaseSettings):
    elyman_database_user:str
    elyman_database_name:str
    elyman_database_server:str = "database-2.c3egd4km892g.us-east-1.rds.amazonaws.com"
    elyman_database_password:str = 'akolo000'
    elyman_secret_key:str = "d329748e4dce05b3fcf429da2bb8914f240ff0c288897f455ae792f82aee3cc0"
    elyman_algorithm:str = "HS256"
    elyman_access_token_expire_minutes:int
    class Config:
        env_file = "./app/.env"

settings = Settings()
