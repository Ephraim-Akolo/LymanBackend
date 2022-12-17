from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .. import schemas, oauth2
from .. import models as db_models
from ..database import get_session

router = APIRouter(
    prefix="/api/v1/products",
    tags=["Products"]
)

@router.post('/orders', status_code=status.HTTP_201_CREATED)
def create_order(order: schemas.Orders, db_session:Session = Depends(get_session), customer_data: schemas.TokenData = Depends(oauth2.get_current_customer)):
    new_purchase = db_models.Purchase(customer_id=customer_data.id)
    db_session.add(new_purchase)
    db_session.commit()
    db_session.refresh(new_purchase)
    try:
        for p, q in order.product_quantity_ids.items():
            new_order = db_models.Order(order_id=new_purchase.order_id, product_id=int(p), quantity=q)
            db_session.add(new_order)
            db_session.commit()
    except SQLAlchemyError as e:
        db_session.rollback()
        db_session.delete(new_purchase)
        db_session.commit()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"no product with id {p} found!")
    return {"customer_id": new_purchase.customer_id, "order_id": new_purchase.order_id}

@router.get('/{quantity}') #response_model=List[schemas.ArtistanResponse] ## from typing import List
def get_products(quantity:int, db_session:Session = Depends(get_session)):
    products = db_session.query(db_models.Product).limit(quantity).all()
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no products found!")
    return products

@router.get('/categories/{category}/{quantity}')
def get_products(category:str, quantity:int, db_session:Session = Depends(get_session)):
    products = db_session.query(db_models.Product).filter(db_models.Product.category == category).limit(quantity).all()
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no products found in category!")
    return products

