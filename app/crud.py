from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import model, schemas
from .auth import hash_password, verify_password

# Register user
async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_pw = hash_password(user.password)
    new_user = model.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# Find user by email
async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(model.User).where(model.User.email == email))
    return result.scalars().first()
