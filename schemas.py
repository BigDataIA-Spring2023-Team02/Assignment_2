from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User_Table(Base):
    __tablename__ = "users"
    ID = Column(Integer, primary_key= True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    password = Column(String)

class User(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str

class Username(BaseModel):
    username: str
    class Config():
        orm_mode = True

class UserInDB(User):
    password: str

class Login(BaseModel):
    username: str
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None