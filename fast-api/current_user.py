from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
import schemas, user_data, user_db_model
from sqlalchemy.orm import Session
from jwt_api import bcrypt, verify, verify_token, create_access_token, get_current_user

router = APIRouter(
    tags = ['users']
)
get_db = user_data.get_db

@router.post('/user/create', response_model= schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = user_db_model.User_Table(full_name = request.full_name, username = request.username, password = bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user