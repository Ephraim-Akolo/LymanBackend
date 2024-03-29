from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, utils, oauth2
from .. import models as db_models
from ..database import get_session

router = APIRouter(
    prefix="/api/v1/customers",
    tags=["Customers"]
)

@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=schemas.CustomerResponse)
def signup_customers(customer: schemas.Customer, db_session:Session = Depends(get_session)):
    if customer.password != customer.confirm_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"unmatched passwords!")
    existing_user = db_session.query(db_models.Customer).filter(db_models.Customer.email == customer.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail=f"customer with email '{customer.email}' already exist!")
    customer.password = utils.hash(customer.password)
    params = customer.dict()
    params.pop("confirm_password")
    new_customer = db_models.Customer(**params)
    db_session.add(new_customer)
    db_session.commit()
    db_session.refresh(new_customer)
    return  new_customer

@router.get("/profile", response_model=schemas.CustomerResponse)
def get_customer_details(db_session:Session = Depends(get_session), customer_data:schemas.TokenData = Depends(oauth2.get_current_customer)):
    customer = db_session.query(db_models.Customer).filter(db_models.Customer.id==customer_data.id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No customer with id ({id}) found!")
    return customer

@router.put("/rating", response_model=schemas.PurchaseResponse)
def update_artistan_rating(artistan_id:int, rating:int, order_id:int, db_session:Session = Depends(get_session), customer_data:schemas.TokenData = Depends(oauth2.get_current_customer)):
    order = db_session.query(db_models.Purchase).filter(db_models.Purchase.order_id == order_id).filter(db_models.Customer.id == customer_data.id)
    artistan = db_session.query(db_models.Artistan).filter(db_models.Artistan.id == artistan_id).first()
    if not artistan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Artistan with id {artistan_id} found!")
    if not order.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No order with id {order_id} found!")
    if rating > 5 or rating < 1:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="'rating' must be in the range of '1' and '5'")
    order.update({db_models.Purchase.artistan_id: artistan_id, db_models.Purchase.rating: rating}, synchronize_session=False)
    db_session.commit()
    return order.first()

