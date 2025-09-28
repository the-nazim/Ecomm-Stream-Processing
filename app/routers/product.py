from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas, crud, auth, model
from app.model import get_db


router = APIRouter(prefix="/products", tags=["products"])

@router.post("/create-product")
async def createProduct(form_data: schemas.ProductCreate, db: AsyncSession = Depends(get_db), currentUser: model.User = Depends(auth.require_role('admin'))):
    new_product = await crud.create_product(db, form_data)
    return {"message": "Product added successfully", "product": new_product}

@router.get("/")
async def listProducts(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    products = await crud.get_products(db, skip=skip, limit=limit)
    return {"products": products}

@router.get("/{product_id}")
async def getProduct(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"product": product}

@router.put("/update-product/{product_id}")
async def updateProduct(product_id: int, form_data: schemas.ProductCreate, db: AsyncSession = Depends(get_db), currentUser: model.User = Depends(auth.require_role('admin'))):
    updateProd = await crud.update_product(db, product_id, form_data) 
    if not updateProd:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product updated successfully", "product": updateProd}

@router.delete("/delete-product/{product_id}")
async def deleteProduct(product_id: int, db: AsyncSession = Depends(get_db), currentUser: model.User = Depends(auth.require_role('admin'))):
    deletedProd = await crud.delete_product(db, product_id)
    if not deletedProd:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully", "product": deletedProd}