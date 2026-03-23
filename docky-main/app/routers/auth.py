import jwt
import os

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from typing import Annotated

from fastapi import HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.exceptions import DoesNotExist, IntegrityError

from app.models import User
from app.schemas import UserCreate, UserOut
from app.schemas import Token

load_dotenv()

router = APIRouter()

ph = PasswordHasher()

@router.post("/register", response_model=UserOut)
async def register_user(user: UserCreate):
  try:
    new_user = await User.create(
      email=user.email,
      name=user.name,
      passwd=ph.hash(user.password)
    )
    return new_user  # Pydantic will auto-convert to UserOut
  except IntegrityError:
    raise HTTPException(status_code=400, detail="Email already registered")
        
# login route
@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
  print("Login attempt:", form_data.username)

  try:
    user = await User.get(email=form_data.username)
    print("User found:", user.email)

    try:
      ph.verify(user.passwd, form_data.password)
      print("Password matched")

      expire = datetime.now(timezone.utc) + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
      payload = {
          "sub": user.email,
          "name": user.name,
          "exp": expire
      }

      access_token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
      print("Access token generated")

      return Token(access_token=access_token, token_type="bearer")

    except VerifyMismatchError:
      print("Password mismatch")
      raise HTTPException(status_code=400, detail="Incorrect username or password")

  except DoesNotExist:
    print("User not found")
    raise HTTPException(status_code=400, detail="Incorrect username or password")