from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from os import getenv

password = getenv('ELYMAN_DATABASE_PASSWORD')
if password is None:
    raise(Exception("Environmental varaible ELYMAN_DATABASE_PASSWORD not set!"))

engine = create_engine(f"mysql+pymysql://root:{password}@localhost/ElymanDB", echo=True)

Session = sessionmaker(bind=engine, autoflush=False)

Base = declarative_base()


def get_session():
    local_session = Session()
    try:
        yield local_session
    finally:
        local_session.close()
