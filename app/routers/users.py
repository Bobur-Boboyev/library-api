from typing import Annotated, List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserRegister, UserResponse
from app.dependencies import get_db
from app.crud.user import get_user_by_username, create_user, get_users
from app.security import hash_password

router = APIRouter(tags=["users"])


@router.post("/api/register", response_model=UserResponse, status_code=201)
async def register_view(
    data: Annotated[UserRegister, Body()],
    db: Annotated[Session, Depends(get_db)],
):
    existing_user = get_user_by_username(db, data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exsists.")

    user = create_user(
        db=db,
        username=data.username,
        hash_password=hash_password(data.password),
    )
    return user


@router.get("/api/users", response_model=List[UserResponse])
async def register_view(db: Annotated[Session, Depends(get_db)]):
    return get_users(db)
