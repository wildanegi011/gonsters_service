"""JWT utils."""


from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")



fake_users_db = {
    "johndoe": {
        "id": 1,
        "username": "johndoe",
        "email": "johndoe@example.com",
        "password": "rahasia123",
        "role": "operator"
    },
    "wildan": {
        "id": 2,
        "username": "wildan",
        "email": "admin@example.com",
        "password": "rahasia123",
        "role": "management"
    },
    "yani": {
        "id": 3,
        "username": "yani",
        "email": "supervisor@example.com",
        "password": "rahasia123",
        "role": "supervisor"
    }
}

class Token(BaseModel):
    """Access token."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data."""

    username: str | None = None


class User(BaseModel):
    """User."""

    id: int
    username: str
    email: str | None = None
    role: str


class UserInDB(User):
    """User in DB."""

    password: str


def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create access token."""
    to_encode = data.copy()
    now = datetime.now(UTC)
    expire = now + expires_delta if expires_delta else now + timedelta(minutes=15)
    to_encode.update({"iat": now.timestamp(), "exp": expire.timestamp(), "iss": "gonsters-services"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user(db, username: str):
    """Get user."""
    print(f"Found user: {db}")
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    """Authenticate user."""
    user = get_user(fake_db, username)
    print(f"Authenticating user: {user}")
    if not user:
        return False
    if user.password != password:
        return False
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """Get current User."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        print(f"Decoded payload: {username}")
        role = payload.get("role")
        if username is None or role is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception  # noqa: B904
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def require_roles(allowed_roles: list[str]):
    """Require a specific role for a route."""
    def role_checker(user: Annotated[User, Depends(get_current_user)]):
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You dont have any permission for access this api")
        return user
    return role_checker
