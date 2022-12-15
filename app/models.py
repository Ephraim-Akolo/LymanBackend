from .database import Base
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, Date

SHORT_STR = 20

LONG_STR = 50

DESCRIPTION = 1000


class DB_Products(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False)

    name = Column(String(SHORT_STR), nullable=False)

    price = Column(Integer, nullable=False)

    image = Column(String(100), nullable=False)

    category = Column(String(SHORT_STR))

    discription = Column(String(DESCRIPTION), nullable=False)

    instock = Column(Boolean, nullable=True)


class DB_Customer(Base):

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, nullable=False)

    first_name = Column(String(SHORT_STR), nullable=False)

    last_name = Column(String(SHORT_STR), nullable=False)

    email = Column(String(LONG_STR), nullable=False, unique=True)

    password = Column(String(LONG_STR), nullable=False)


class DB_Artistan(Base):

    __tablename__ = "artistans"

    id = Column(Integer, primary_key=True, nullable=False)

    first_name = Column(String(SHORT_STR), nullable=False)

    last_name = Column(String(SHORT_STR), nullable=False)

    email = Column(String(LONG_STR), nullable=False, unique=True)

    password = Column(String(LONG_STR), nullable=False)

    qualification = Column(String(SHORT_STR), nullable=False)

    birth_date = Column(Date)


class DB_Purchase(Base):

    __tablename__ = "purchases"

    order_id = Column(Integer, primary_key=True, nullable=False)

    customer_id = Column(Integer, ForeignKey('customers.id', ondelete="CASCADE"), nullable=False)

    artistan_id = Column(Integer, ForeignKey('artistans.id', ondelete="CASCADE"), nullable=True)

    rating = Column(Integer)

    


class DB_Order(Base):
    
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, nullable=False)

    order_id = Column(Integer, ForeignKey('purchases.order_id', ondelete="CASCADE"), nullable=False)

    product_id = Column(Integer, ForeignKey('products.id', ondelete="CASCADE"), nullable=False)

    quantity = Column(Integer, nullable=False)

    shipped = Column(Boolean, default=False)

    delivered = Column(Boolean, default=False)

