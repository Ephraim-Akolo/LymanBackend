from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, utils, oauth2, machinelearning
from typing import List
from .. import models as db_models
from ..database import get_session

router = APIRouter(
    prefix="/api/v1/artistans",
    tags=["Artistans"]
)

@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=schemas.ArtistanResponse)
def signup_artistan(artistan: schemas.Artistan, db_session:Session = Depends(get_session)):
    if artistan.password != artistan.confirm_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"unmatched passwords!")
    artistan.password = utils.hash(artistan.password)
    params = artistan.dict()
    params.pop("confirm_password")
    new_artistan = db_models.Artistan(**params)
    db_session.add(new_artistan)
    db_session.commit()
    db_session.refresh(new_artistan)
    return new_artistan

@router.get("/profile", response_model=schemas.CustomerResponse)
def get_artistan_details(db_session:Session = Depends(get_session), artistan_data:schemas.TokenData = Depends(oauth2.get_current_artistan)):
    artistan = db_session.query(db_models.Artistan).filter(db_models.Artistan.id==artistan_data.id).first()
    if not artistan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No artistan with id ({id}) found!")
    return artistan

@router.get('/recommender/{quantity}', response_model=List[schemas.ArtistanResponse])
def recommend_artistans(quantity:int,  db_session:Session = Depends(get_session), customer_data:schemas.TokenData = Depends(oauth2.get_current_customer)):
    return machinelearning.predictor(customer_data.id, db_session, quantity)

