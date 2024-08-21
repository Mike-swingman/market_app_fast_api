from fastapi import APIRouter, HTTPException, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.schemas import UserAuthSchema
from app.users.models import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=201)
async def register(user_data: UserAuthSchema, session: AsyncSession = Depends(get_db)):
    existing_user = await User.get_or_none(session, email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=400)
    hashed_password = get_password_hash(user_data.password)
    await User.add(session, email=user_data.email, hashed_password=hashed_password)
    return {
        "status_code": 201,
        "detail": "Registration successful",
    }


@router.post("/login")
async def login(
    response: Response, user_data: UserAuthSchema, session: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(session, user_data.email, user_data.password)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
