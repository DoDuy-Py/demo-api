from typing import Optional

from pydantic import BaseModel

from core.settings import settings
import jwt
from fastapi import APIRouter, Depends, HTTPException, Request, status

from datetime import datetime, timezone


class TokenData(BaseModel):
    id: Optional[int] = None
    roles: list = []


def validate_token(auth: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = auth.split(" ")[1]  # Lấy token từ header 'Bearer <token>'
        # Giải mã token và lấy thông tin người dùng
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.SECURITY_ALGORITHM])
            user = payload.get("user")
            exp = payload.get("exp")
            if not user or not exp:
                raise credentials_exception
            elif datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(tz=timezone.utc):
                raise credentials_exception
            user = TokenData(**user)
            return user
        except jwt.PyJWTError:
            raise credentials_exception
    except Exception as e:
        print(e)
        return None