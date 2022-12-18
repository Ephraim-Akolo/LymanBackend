from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from os import getenv

name = getenv('ELYMAN_DATABASE_NAME')
password = getenv('ELYMAN_DATABASE_PASSWORD')
user = getenv('ELYMAN_DATABASE_USER')
server = getenv('ELYMAN_DATABASE_SERVER')
if name is None:
    raise(Exception("Environmental varaible ELYMAN_DATABASE_NAME not set!"))
if password is None:
    raise(Exception("Environmental varaible ELYMAN_DATABASE_PASSWORD not set!"))
if user is None:
    raise(Exception("Environmental varaible ELYMAN_DATABASE_USER not set!"))
if server is None:
    raise(Exception("Environmental varaible ELYMAN_DATABASE_SERVER not set!"))

engine = create_engine(f"mysql+pymysql://{user}:{password}@{server}/{name}", echo=True)

Session = sessionmaker(bind=engine, autoflush=False)

Base = declarative_base()


def get_session():
    local_session = Session()
    try:
        yield local_session
    finally:
        local_session.close()
