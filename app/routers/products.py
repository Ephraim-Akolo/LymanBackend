from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from .. import schemas, oauth2
from .. import models as db_models
from ..database import get_session

router = APIRouter(
    prefix="/api/v1/products",
    tags=["Products"]
)

@router.get('/', response_model=List[schemas.ProductsResponse]) #response_model=List[schemas.ArtistanResponse] ## from typing import List
def get_products(db_session:Session = Depends(get_session), category:str="", search:str="", limit:int=20, skip:int=0):
    products = db_session.query(db_models.Product)
    if category != "":
        products = products.filter(db_models.Product.category.contains(category))
    if search != '':
        products = products.filter(or_(db_models.Product.name.contains(search), db_models.Product.discription.contains(search)))
    products = products.limit(limit).offset(skip).all()
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no products found!")
    return products

@router.get('/orders/{order_id}', response_model=List[schemas.OrderResponse])
def get_orders(order_id:int, db_session:Session = Depends(get_session), customer_data: schemas.TokenData = Depends(oauth2.get_current_customer)):
    orders = db_session.query(db_models.Order).join(db_models.Purchase).filter(db_models.Purchase.customer_id == customer_data.id, db_models.Order.order_id == order_id).all()
    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"you have no orders with id {order_id}!")
    return orders
    

@router.post('/orders', status_code=status.HTTP_201_CREATED, response_model=schemas.PurchaseResponse)
def create_order(order: schemas.Orders, db_session:Session = Depends(get_session), customer_data: schemas.TokenData = Depends(oauth2.get_current_customer)):
    new_purchase = db_models.Purchase(customer_id=customer_data.id)
    db_session.add(new_purchase)
    db_session.commit()
    db_session.refresh(new_purchase)
    try:
        for p, q in order.product_quantity_ids.items():
            if p < 0 or q < 0:
                raise SQLAlchemyError
            new_order = db_models.Order(order_id=new_purchase.order_id, product_id=p, quantity=q)
            db_session.add(new_order)
            db_session.commit()
    except SQLAlchemyError:
        db_session.rollback()
        db_session.delete(new_purchase)
        db_session.commit()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"no product with id {p} found!")
    return new_purchase
