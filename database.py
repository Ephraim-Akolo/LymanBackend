from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("mysql+pymysql://root:akolo000@localhost/DeleteMe", echo=True)

Session = sessionmaker(bind=engine, autoflush=False)

Base = declarative_base()


def get_session():
    local_session = Session()
    try:
        yield local_session
    finally:
        local_session.close()
