from datetime import timedelta, datetime

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import jwt

from app.entity.models import Usuario
from app.entity.schema import UsuarioInDB
from app.controller import database


SECRET_KEY = "99549bdea40fcfb8918ff38673528638f68c039befabe3338012e3c2467913c9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def create_usuario(item: Usuario):
    item.password = get_password_hash(item.password)
    usuario = await database.create_usuario(item)
    return usuario


async def get_usuario(username: str) -> UsuarioInDB | None:
    usuario = await database.get_usuario(username)
    return usuario


async def authenticate_user(username: str, password: str):
    usuario = await get_usuario(username)
    if not usuario:
        return False
    if not verify_password(password, usuario.password):
        return False
    return usuario


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Credenciais não validadas.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.exceptions.PyJWTError:
        raise credentials_exception
    usuario = await get_usuario(username=username)
    if usuario is None:
        raise credentials_exception
    return usuario


async def get_current_active_user(current_user: Usuario = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
