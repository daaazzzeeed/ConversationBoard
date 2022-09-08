from fastapi import APIRouter
from fastapi.exceptions import RequestValidationError
from pydantic.error_wrappers import ErrorWrapper

from app.apps.users.schemas import UserCreate, Token
from app.db import Session
from app.apps.users.models import User
from app.utils import get_hashed_password, verify_password, create_access_token, create_refresh_token

users_router = APIRouter(prefix="/users")


@users_router.post("/sign_up/", response_model=UserCreate)
def create_user(data: UserCreate):
    session = Session()
    user = session.query(User).get(data.login)
    if user is not None:
        error = ErrorWrapper(ValueError(f"User with username={data.login} already exists"), ("query", "login"))
        raise RequestValidationError(errors=[error])
    user = User(login=data.login, password=get_hashed_password(data.password))
    session.add(user)
    session.commit()
    return data


@users_router.post("/sign_in/", response_model=Token)
def login_user(data: UserCreate):
    session = Session()
    user = session.query(User).get(data.login)
    if user is None:
        error = ErrorWrapper(ValueError(f"User with username={data.login} does not exist"), ("query", "login"))
        raise RequestValidationError(errors=[error])
    if not verify_password(data.password, user.password):
        error = ErrorWrapper(ValueError("Invalid password"), ("query", "password"))
        raise RequestValidationError(errors=[error])
    return Token(access_token=create_access_token(user.login), refresh_token=create_refresh_token(user.login))
