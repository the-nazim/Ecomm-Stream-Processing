import asyncio
from fastapi import FastAPI, Request, Form
from contextlib import asynccontextmanager
from model import create_db_and_tables
from settings import settings
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    await create_db_and_tables()
    yield
    # Shutdown code (if needed)

app = FastAPI(lifespan=lifespan, title=settings.APP_NAME)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 templates
templates = Jinja2Templates(directory="templates")

# @app.get("/")
# async def root():
#     return {"message": "E-Commerce API Running"}

# Fake product data
products = [
    {"id": 1, "name": "Laptop", "price": 800},
    {"id": 2, "name": "Phone", "price": 500},
    {"id": 3, "name": "Headphones", "price": 100},
]

cart = []

# In-memory cart for demo (use database in production)
fake_cart_db = [
    {"id": 1, "name": "Laptop", "price": 800},
    {"id": 2, "name": "Phone", "price": 500},
    {"id": 3, "name": "Headphones", "price": 100},
]

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/products", response_class=HTMLResponse)
async def products(request: Request):
    return templates.TemplateResponse("products.html", {"request": request})

@app.get("/product/{product_id}", response_class=HTMLResponse)
async def product_detail(request: Request, product_id: str):
    return templates.TemplateResponse("product-detail.html", {
        "request": request,
        "product_id": product_id
    })

@app.get("/cart", response_class=HTMLResponse)
async def cart(request: Request):
    return templates.TemplateResponse("cart.html", {"request": request})

# API Endpoint to add to cart
@app.post("/api/cart/add")
async def add_to_cart(request: Request):
    data = await request.json()
    # In real app: validate, save to DB, etc.
    fake_cart_db.append(data)
    # Return new cart count
    return str(len(fake_cart_db))  # Return as string for htmx swap

# API Endpoint to get cart count
@app.get("/api/cart/count")
async def get_cart_count():
    return str(len(fake_cart_db))  # Return as string for direct innerHTML

# API Endpoint to get cart items (for cart page)
@app.get("/api/cart/items")
async def get_cart_items():
    return fake_cart_db