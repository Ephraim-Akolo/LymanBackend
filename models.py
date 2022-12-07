from .database import Base
from sqlalchemy import Column, Integer, ForeignKey, String


class Purchase(Base):

    __tablename__ = "purchase"

    id = Column(Integer, primary_key=True, nullable=False)

    customer_id = ForeignKey()

    items = Column(String, nullable=False)

    worker_id = ForeignKey()

    rating = Column(Integer)


class Item(Base):

    __tablename__ = "item"

    id = Column(Integer, primary_key=True, nullable=False)

    name = Column(String, nullable=False)

    price = Column(Integer, nullable=False)

    image = Column(String, nullable=False)

    category = Column(String, nullable=False)


class Customer(Base):

    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, nullable=False)

    first_name = Column(String, nullable=False)

    last_name = Column(String, nullable=False)

    email = Column(String, nullable=False, unique=True)

    image = Column(String, nullable=False)


class Worker(Base):

    __tablename__ = "worker"

    id = Column(Integer, primary_key=True, nullable=False)

    first_name = Column(String, nullable=False)

    last_name = Column(String, nullable=False)

    email = Column(String, nullable=False, unique=True)

    image = Column(String, nullable=False)

    pay = Column(Integer, nullable=False)

