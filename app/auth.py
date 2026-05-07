from .db import SessionDep
from .models import User
from fastapi import APIRouter,Depends
from sqlalchemy import or_
from fastapi.exceptions import HTTPException
from fastapi import status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from .security import (
    pwd_context,
    authenticate,
    create_token,
    verify_token,
    oauth2_scheme,
)
from .schemas import UserDisplay, UserCreate


auth_router = APIRouter(prefix='/auth',tags=['auth'])


@auth_router.post('/register/',response_model=UserDisplay,status_code=status.HTTP_201_CREATED)
async def register(user:UserCreate,db:SessionDep):
    #check if the user already exists
    user_db = db.query(User).filter(   
        or_(
            User.email == user.email,
            User.username == user.username,
        )
    ).first()
    if user_db:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="user with this username/email is already registered")
    
    #we create a new user
    user_data = user.model_dump()
    user_data["password"] = pwd_context.hash(user.password)   #hash the password
    user_db = User(**user_data)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db



@auth_router.post('/login/')
async def login(form_data : Annotated[OAuth2PasswordRequestForm,Depends()],db:SessionDep):
    #authenticate the user
    user = authenticate(form_data.username,form_data.password,db)
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail='we could not authenticate you, verify your username or password'
        )

    #generate token
    data = {
        'sub' : user.email,   #we use the email for the token
    }
    token = create_token(data)
    return {
        "access_token" : token,
        "token_type" : "bearer"
    }


    
def current_user(token: Annotated[str, Depends(oauth2_scheme)], db: SessionDep):
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    email = payload['sub']  #retrieve the email from the decoded token

    user = db.query(User).filter(User.email==email).first()  #search for the user with the email
    return user