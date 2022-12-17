from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, utils, oauth2
from .. import models as db_models
from ..database import get_session

router = APIRouter(
    prefix="/api/v1/login",
    tags=["Authentication"]
)

@router.post('/customers', response_model=schemas.Token)
def login_customer(customer_cred: OAuth2PasswordRequestForm = Depends(), db_session:Session = Depends(get_session)):
    customer = db_session.query(db_models.Customer).filter(db_models.Customer.email == customer_cred.username).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials!")
    if not utils.verify(customer_cred.password, customer.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials!")
    access_token = oauth2.create_access_token(data={"user_id": customer.id, "user_type": db_models.Customer.__tablename__})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/artistans', response_model=schemas.Token)
def login_artistan(artistan_cred: OAuth2PasswordRequestForm = Depends(), db_session:Session = Depends(get_session)):
    artistan = db_session.query(db_models.Artistan).filter(db_models.Artistan.email == artistan_cred.username).first()
    print("one is best")
    if not artistan:
        print("two is best")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials!")
    if not utils.verify(artistan_cred.password, artistan.password):
        print("three is best")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials!")
    access_token = oauth2.create_access_token(data={"user_id": artistan.id, "user_type": db_models.Artistan.__tablename__})
    return {"access_token": access_token, "token_type": "bearer"}
