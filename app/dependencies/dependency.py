from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI,status,HTTPException
from app.exceptions.exception import AuthenticationError,UserNotFoundError,AuthorizationError
from app.security.auth_security import verify_access_token
from fastapi import Depends
from app.db.connection import get_db
from sqlalchemy.orm import Session
from app.repository.user_repository import fetch_user_by_id
OAuth2scheme=OAuth2PasswordBearer(tokenUrl="/user/login")

def get_current_user(
    token: str = Depends(OAuth2scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = verify_access_token(token)
    except AuthenticationError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    try:
       user_id = int(payload.get("sub"))
    except (KeyError,ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid token payload"
        )

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = fetch_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if user.status != "active":
        raise HTTPException(status_code=403, detail="Inactive user")
    return user


def require_admin(
    current_user = Depends(get_current_user)
):
    if current_user.role.upper() != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return current_user

