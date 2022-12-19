from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .utils import settings


engine = create_engine(f"mysql+pymysql://{settings.elyman_database_user}:{settings.elyman_database_password}@{settings.elyman_database_server}/{settings.elyman_database_name}", echo=True)

Session = sessionmaker(bind=engine, autoflush=False)

Base = declarative_base()


def get_session():
    local_session = Session()
    try:
        yield local_session
    finally:
        local_session.close()
