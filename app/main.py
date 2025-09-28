import asyncio
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.model import create_db_and_tables, engine, Base, get_db
from app import settings, schemas, crud, auth, model
from streams.events import send_order_event
from app.routers import product_router, cart_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    await create_db_and_tables()
    yield
    # Shutdown code (if needed)

app = FastAPI(lifespan=lifespan)

app.include_router(product_router)
app.include_router(cart_router)

# Mount static files
# app.mount("/app/static", StaticFiles(directory="static"), name="static")

# Jinja2 templates
# templates = Jinja2Templates(directory="templates")


# ========== Auth Routes ==========
@app.post("/register", response_model=schemas.UserOut)
async def register(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(db, user)


@app.post("/login")
async def login(form_data: schemas.UserLogin, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user_by_email(db, form_data.email)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = auth.create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

# ========== Orders Routes ==========
@app.post("/buy")
async def placeOrder(db: AsyncSession = Depends(get_db), currentUser: model.User = Depends(auth.require_role('customer'))):
    user_id = currentUser.id
    result = await db.execute(select(model.CartItem).where(model.CartItem.user_id == user_id))
    cart_items = result.scalars().all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    newOrder = model.Order(user_id=user_id, status='PENDING')
    db.add(newOrder)
    await db.flush()

    for item in cart_items:
        order_item = model.OrderItem(
            order_id=newOrder.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(order_item)
        
        product = await db.get(model.Product, item.product_id)
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.name}")
        
        product.stock -= item.quantity
        await db.delete(item)
    
    await db.commit()
    await db.refresh(newOrder)
    await send_order_event(newOrder.id, user_id, newOrder.status)

    return {"message": "Order placed successfully", "order_id": newOrder.id}

@app.post("/cancel/{order_id}")
async def cancelOrder(order_id: int, user_id: int=1, db:AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(model.Order)
        .options(selectinload(model.Order.items))
        .where(model.Order.id == order_id)
    )
    order = result.scalars().first()
    if not order or order.user_id != user_id:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status != 'PENDING':
        raise HTTPException(status_code=400, detail="Only pending orders can be cancelled")
    
    for item in order.items:
        product = await db.get(model.Product, item.product_id)
        product.stock += item.quantity
    
    order.status = 'CANCELLED'
    await db.commit()
    await db.refresh(order)
    return {"message": "Order cancelled successfully"}

@app.get("/orders")
async def listOrders(user_id: int=1, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(model.Order).where(model.Order.user_id == user_id))
    orders = result.scalars().all()
    return {"orders": orders}