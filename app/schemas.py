from pydantic import BaseModel, EmailStr, Field

# ========== User ==========
class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: str = Field(default='customer')

class UserCreate(UserBase):   # For input when creating a new user
    password: str

class UserOut(UserBase):      # For output when returning user data
    id: int
    class Config:
        orm_mode = True   # allows converting SQLAlchemy model -> Pydantic schema

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ========== Product ==========
class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    category: str
    stock: int

class ProductCreate(ProductBase):   # For input when creating a product
    pass

class ProductOut(ProductBase):      # For output when returning product data
    id: int
    class Config:
        orm_mode = True

# ========== Cart Item ==========
class CartItemBase(BaseModel):
    product_id: int
    quantity: int = 1

class CartItemCreate(CartItemBase):  # For input when adding item to cart
    pass

class CartItemOut(CartItemBase):     # For output when returning cart item data
    id: int
    user_id: int
    class Config:
        orm_mode = True