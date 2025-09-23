import asyncio
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from contextlib import asynccontextmanager
from model import create_db_and_tables, engine, Base, get_db
from settings import settings
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from fastapi.security import OAuth2PasswordRequestForm
import schemas, crud, auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    await create_db_and_tables()
    yield
    # Shutdown code (if needed)

app = FastAPI(lifespan=lifespan, title=settings.APP_NAME)

# Mount static files
app.mount("/app/static", StaticFiles(directory="static"), name="static")

# Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Fake product data
products = [
    {"id": 1, "name": "Laptop", "price": 800},
    {"id": 2, "name": "Phone", "price": 500},
    {"id": 3, "name": "Headphones", "price": 100},
]

cart = []


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

# ========== Product Routes ==========
@app.post("/create-product")
async def createProduct(form_data: schemas.ProductCreate, db: AsyncSession = Depends(get_db)):
    new_product = await crud.create_product(db, form_data)
    return {"message": "Product added successfully", "product": new_product}

@app.get("/products")
async def listProducts(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    products = await crud.get_products(db, skip=skip, limit=limit)
    return {"products": products}

@app.get("/products/{product_id}")
async def getProduct(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"product": product}

@app.put("/update-product/{product_id}")
async def updateProduct(product_id: int, form_data: schemas.ProductCreate, db: AsyncSession = Depends(get_db)):
    updateProd = await crud.update_product(db, product_id, form_data) 
    if not updateProd:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product updated successfully", "product": updateProd}

@app.delete("/delete-product/{product_id}")
async def deleteProduct(product_id: int, db: AsyncSession = Depends(get_db)):
    deletedProd = await crud.delete_product(db, product_id)
    if not deletedProd:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully", "product": deletedProd}

# ========== Cart Routes ==========
@app.post("/add-to-cart")
async def addToCart(form_data: schemas.CartItemCreate, db: AsyncSession = Depends(get_db), user_id: int=1):
    return await crud.add_to_cart(db, user_id, form_data)

@app.delete("/remove/{product_id}")
async def removeFromCart(product_id: int, db: AsyncSession = Depends(get_db), user_id: int=1):
    result = await crud.remove_from_cart(db, user_id, product_id)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    return {"message":"Item successfully removed"}

@app.get("/cart")
async def getCart(db: AsyncSession = Depends(get_db), user_id: int=1):
    return await crud.get_cart(db, user_id)
