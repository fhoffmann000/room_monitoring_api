from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import get_db
from .. import schemas, models, utils, oauth2


router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    if user.usertype == "readonly":
        new_logindata = models.Login_History(user_id=user.id, login_timestamp = datetime.utcnow())
        db.add(new_logindata)
        db.commit()
        db.refresh(new_logindata)

    return {"access_token": access_token, "token_type": "bearer"}
