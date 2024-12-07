from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserResponse(BaseModel):
    id: int
    username: str
    usertype: str
    created_at: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class DataCreate(BaseModel):
    location: str
    temperature: float
    air_quality: float
    humidity: float

class DataResponse(BaseModel):
    id: int
    location: str
    temperature: float
    air_quality: float
    humidity: float
    created_at: datetime
    owner_id: int
    #owner: UserResponse

    class Config:
        orm_mode = True

class LoginCreate(BaseModel):
    login_datestamp: datetime
    user_id: int

class LoginResponse(BaseModel):
    id: int
    login_datestamp: datetime
    user_id: int

    class Config:
        orm_mode = True