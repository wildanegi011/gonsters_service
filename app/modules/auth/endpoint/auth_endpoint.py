"""Auth endpoint."""

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.modules.auth.service.auth_service import AuthService
from app.utils.utlis import User, get_current_user, require_roles

router = APIRouter(
    tags=["auth"]
)

def get_auth_service():
    """Get auth service."""
    return AuthService()


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: Annotated[AuthService, Depends(get_auth_service)]
):
    """Login."""
    return await service.login(form_data)

@router.get("/users/me/")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Read user."""
    return current_user


@router.post("/api/v1/config/update")
def update_config(user: Annotated[User, Depends(require_roles("management"))]):
    """Update configuration endpoint."""
    return {"status": "success", "user": user.username, "message": "Configuration updated successfully"}
