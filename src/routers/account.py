from src.services.account import get_hashed_password, verify_password, create_access_token, create_refresh_token
from src.schemas.account import UserCreate, UserLogin, Token, UserResponse
from config.database.db_helper import db_helper
from fastapi import APIRouter, HTTPException
from src.models.base_model import User
from sqlalchemy import select
import re


router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    email = user.email.lower()
    async with db_helper.get_db_session() as db:
        existing_user = await db.execute(select(User).where(User.email == email))
        if existing_user.fetchone():
            raise HTTPException(status_code=400, detail="Пользователь с такой почтой уже существует")

        password = user.password
        if not re.match(r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{6,}$", password):
            raise HTTPException(status_code=400,
                                detail="Пароль должен состоять минимум из 6 символов, иметь хотя бы одну заглавную букву, одну цифру и один специальный символ")

        hashed_password = get_hashed_password(password).encode('utf-8')
        db_user = User(email=email, hashed_password=hashed_password, full_name=user.full_name, is_active=False)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

    return db_user


@router.post("/login", response_model=Token)
async def login_user(user: UserLogin):
    async with db_helper.get_db_session() as db:
        db_user = await db.execute(select(User).where(User.email == user.email))
        db_user = db_user.scalar()
        if not db_user or not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(status_code=400, detail="Неверный логин или пароль")
        access_token = create_access_token(str(db_user.id))
        refresh_token = create_refresh_token(str(db_user.id))
        return Token(access_token=access_token, refresh_token=refresh_token, token_type="Bearer")

