from fastapi import FastAPI, Response, status, HTTPException, Depends
from . import schemas
from . import models as db_models
from app.database import get_session, engine, Base
from sqlalchemy.orm import Session

Base.metadata.create_all(engine)

app = FastAPI()

@app.get('/')
def root():
    return {'message': "Application Running"}

@app.post('/v1/customers', status_code=status.HTTP_201_CREATED)
def signup_customers(customer: schemas.Customer, db_session:Session = Depends(get_session)):
    if customer.password != customer.confirm_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"unmatched passwords!")
    params = customer.dict()
    params.pop("confirm_password")
    new_customer = db_models.DB_Customer(**params)
    db_session.add(new_customer)
    db_session.commit()
    db_session.refresh(new_customer)
    return  new_customer

@app.post('/v1/customers/login')
def login_customer(customer: schemas.Authenticate):
    # authenticate customer
    return # authenticated customer

@app.post('/v1/artistans', status_code=status.HTTP_201_CREATED)
def signup_artistan(artistan: schemas.Artistan, db_session:Session = Depends(get_session)):
    if artistan.password != artistan.confirm_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"unmatched passwords!")
    params = artistan.dict()
    params.pop("confirm_password")
    new_artistan = db_models.DB_Artistan(**params)
    db_session.add(new_artistan)
    db_session.commit()
    db_session.refresh(new_artistan)
    return new_artistan

@app.post('/v1/artistans/login')
def login_artistan(artistan: schemas.Authenticate):
    # authenticate customer
    return # authenticated customer

@app.get('/v1/artistans/recommender/{user_id}/{quantity}')
def recommend_artistans(user_id:int, quantity:int):
    # rank artistans based on last found order
    return # top "quantity" of artistans

@app.post('/v1/products/orders', status_code=status.HTTP_201_CREATED)
def create_order(order: schemas.Orders, db_session:Session = Depends(get_session)):
    new_purchase = db_models.DB_Purchase(customer_id=order.customer_id)
    db_session.add(new_purchase)
    db_session.commit()
    db_session.refresh(new_purchase)
    for p, q in order.product_quantity_ids.items():
        new_order = db_models.DB_Order(order_id=new_purchase.order_id, product_id=int(p), quantity=q)
        db_session.add(new_order)
        db_session.commit()
    return {"order_id": new_purchase.order_id}

@app.get('/v1/products/{quantity}')
def get_products(quantity:int, db_session:Session = Depends(get_session)):
    products = db_session.query(db_models.DB_Products).limit(quantity).all()
    return products

@app.get('/v1/products/categories/{category}/{quantity}')
def get_products(category:str, quantity:int, db_session:Session = Depends(get_session)):
    products = db_session.query(db_models.DB_Products).filter(db_models.DB_Products.category == category).limit(quantity).all()
    return products

