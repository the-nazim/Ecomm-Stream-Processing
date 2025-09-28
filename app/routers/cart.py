from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas, crud, model
from app.model import get_db

router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/add-to-cart")
async def addToCart(form_data: schemas.CartItemCreate, db: AsyncSession = Depends(get_db), user_id: int=1):
    return await crud.add_to_cart(db, user_id, form_data)

@router.delete("/remove/{product_id}")
async def removeFromCart(product_id: int, db: AsyncSession = Depends(get_db), user_id: int=1):
    result = await crud.remove_from_cart(db, user_id, product_id)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    return {"message":"Item successfully removed"}

@router.get("/")
async def getCart(db: AsyncSession = Depends(get_db), user_id: int=1):
    return await crud.get_cart(db, user_id)