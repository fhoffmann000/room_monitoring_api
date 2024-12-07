from .database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class Data_Point(Base):
    __tablename__ = "room_data"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    location = Column(String, nullable=True)
    temperature = Column(Float, nullable=False)
    air_quality = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=False)

    #owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    usertype = Column(String, nullable=False, server_default="readonly")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Login_History(Base):
    __tablename__ = "login_history"

    id = Column(Integer, primary_key=True, nullable=False)
    login_timestamp = Column(TIMESTAMP(timezone=True), nullable=False)
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    #owner = relationship("User")