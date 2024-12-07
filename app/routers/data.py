from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional


from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/data",
    tags=["Data"]
)


@router.get("", response_model=List[schemas.DataResponse])
def get_data(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, offset: int = 0):

    data = db.query(models.Data_Point).order_by("id").limit(limit).offset(offset).all()
    return data

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.DataResponse)
def create_data_point(data: schemas.DataCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    if current_user.usertype != "write":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform request: You're read only.")

    new_data = models.Data_Point(owner_id=current_user.id, **data.dict())
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data