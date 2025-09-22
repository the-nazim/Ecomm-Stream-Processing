from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import model, schemas
from auth import hash_password, verify_password


# ========== User Management ==========
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


# ========== Product Management ==========
async def create_product(db: AsyncSession, product: schemas.ProductCreate):
    new_product = model.Product(**product.dict())
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product

async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(model.Product).where(model.Product.id == product_id))
    return result.scalars().first()

async def get_products(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(model.Product).offset(skip).limit(limit))
    return result.scalars().all()

async def update_product(db: AsyncSession, product_id: int, product: schemas.ProductCreate):
    currProduct = await get_product(db, product_id)
    if not currProduct:
        return None
    for key, value in product.dict().items():
        setattr(currProduct, key, value)
    await db.commit()
    await db.refresh(currProduct)
    return currProduct

async def delete_product(db: AsyncSession, product_id: int):
    currProduct = await get_product(db, product_id)
    if not currProduct:
        return None
    await db.delete(currProduct)
    await db.commit()
    return currProduct