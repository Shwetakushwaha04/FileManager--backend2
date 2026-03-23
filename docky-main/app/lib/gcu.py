import jwt
import os
from typing import Annotated
from dotenv import load_dotenv

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from app.models.user import User
from app.schemas.user import UserSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

load_dotenv()

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )
  try:
    payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
    email = payload.get("sub")
    if email is None:
      raise credentials_exception
    user = await UserSession.from_queryset_single(User.get(email=email))
    return user
  except InvalidTokenError:
    raise credentials_exception

gcu = Annotated[UserSession, Depends(get_current_user)]
