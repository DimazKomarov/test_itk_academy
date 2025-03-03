from datetime import datetime, timezone, timedelta
from typing import Annotated

import bcrypt
import jwt
from jwt.exceptions import InvalidTokenError

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core.config import settings


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)


def get_current_token_payload(
        token: Annotated[str, Depends(oauth2_scheme)]
) -> dict:
    try:
        payload = decode_jwt(token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен!",
        )
    return payload


def encode_jwt(payload: dict) -> str:
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        to_encode,
        settings.PRIVATE_KEY_PATH.read_text(),
        algorithm=settings.ALGORITHM,
    )
    return encoded


def decode_jwt(token: str | bytes) -> dict:
    decoded = jwt.decode(
        token,
        settings.PUBLIC_KEY_PATH.read_text(),
        algorithms=[settings.ALGORITHM],
    )
    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )
