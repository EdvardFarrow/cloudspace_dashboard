from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import schemas, models, security
from app.auth.dependencies import get_current_user, get_current_admin
from app.core.database import get_async_session
from sqlalchemy import select

router = APIRouter(prefix="/auth", tags=["auth"])

# Регистрация нового пользователя (только админ)
@router.post("/register", response_model=schemas.UserOut)
async def register_user(
    user_in: schemas.UserCreate,
    session: AsyncSession = Depends(get_async_session),
    current_admin: models.User = Depends(get_current_admin),
):
    # Проверяем, что email уникален
    existing = await session.execute(
        models.User.__table__.select().where(models.User.email == user_in.email)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = security.get_password_hash(user_in.password)
    new_user = models.User(
        email=user_in.email,
        hashed_password=hashed_password,
        full_name=user_in.full_name,
        role=user_in.role
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

# Вход — получение JWT токена
@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    # Ищем пользователя по email
    result = await session.execute(
        select(models.User).where(models.User.email == form_data.username)
    )
    user = result.scalars().first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(data={"sub": user.email})
    return schemas.Token(access_token=access_token, token_type="bearer")

# Текущий пользователь
@router.get("/me", response_model=schemas.UserOut)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user
