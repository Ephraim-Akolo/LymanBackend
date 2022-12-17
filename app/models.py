from .database import Base
from sqlalchemy import Column, Integer, Float, ForeignKey, String, Boolean, Date, TIMESTAMP, text

SHORT_STR = 20

LONG_STR = 100

DESCRIPTION = 1000


class Product(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False)

    name = Column(String(SHORT_STR), nullable=False)

    price = Column(Float, nullable=False)

    image = Column(String(100), nullable=False)

    category = Column(String(SHORT_STR))

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    discription = Column(String(DESCRIPTION), nullable=False)

    instock = Column(Boolean, nullable=True)


class Customer(Base):

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, nullable=False)

    first_name = Column(String(SHORT_STR), nullable=False)

    last_name = Column(String(SHORT_STR), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    email = Column(String(LONG_STR), nullable=False, unique=True)

    password = Column(String(LONG_STR), nullable=False)


class Artistan(Base):

    __tablename__ = "artistans"

    id = Column(Integer, primary_key=True, nullable=False)

    first_name = Column(String(SHORT_STR), nullable=False)

    last_name = Column(String(SHORT_STR), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    email = Column(String(LONG_STR), nullable=False, unique=True)

    password = Column(String(LONG_STR), nullable=False)

    qualification = Column(String(SHORT_STR), nullable=False)

    birth_date = Column(Date)


class Purchase(Base):

    __tablename__ = "purchases"

    order_id = Column(Integer, primary_key=True, nullable=False)

    customer_id = Column(Integer, ForeignKey('customers.id', ondelete="CASCADE"), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    artistan_id = Column(Integer, ForeignKey('artistans.id', ondelete="CASCADE"), nullable=True)

    rating = Column(Integer)

    


class Order(Base):
    
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, nullable=False)

    order_id = Column(Integer, ForeignKey('purchases.order_id', ondelete="CASCADE"), nullable=False)

    product_id = Column(Integer, ForeignKey('products.id', ondelete="CASCADE"), nullable=False)

    quantity = Column(Integer, nullable=False)

    shipped = Column(Boolean, default=False)

    delivered = Column(Boolean, default=False)

