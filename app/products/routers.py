from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.products.schemas import ProductSchema, ProductUpdateSchema, ProductFilterSchema
from app.products.models import Product

router = APIRouter(prefix="/products", tags=["Product"])


@router.post("/", response_model=ProductSchema)
async def add(
    data: ProductSchema, session: AsyncSession = Depends(get_db)
) -> ProductSchema:
    return await Product.add(
        session,
        name=data.name,
        description=data.description,
        quantity=data.quantity,
        price=data.price,
        category_id=data.category_id,
    )


@router.get("/{product_id}", response_model=ProductSchema)
async def get(
    product_id: int, session: AsyncSession = Depends(get_db)
) -> ProductSchema:
    product = await Product.get_or_none(session, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.delete("/{product_id}")
async def delete(product_id: int, session: AsyncSession = Depends(get_db)) -> None:
    try:
        return await Product.delete(session, id=product_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{product_id}")
async def update(
    product_id: int, data: ProductUpdateSchema, session: AsyncSession = Depends(get_db)
):
    return await Product.update_product(product_id, data, session)


@router.post("/filter_by", response_model=List[ProductSchema])
async def get_filtered_products(
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    min_quantity: Optional[int] = None,
    name_pattern: Optional[str] = None,
    category_id: Optional[int] = None,
    session: AsyncSession = Depends(get_db),
):
    filters = ProductFilterSchema(
        min_price=min_price,
        max_price=max_price,
        min_quantity=min_quantity,
        name_pattern=name_pattern,
        category_id=category_id
    )
    products = await Product.filter_products(session, filters)

    if not products:
        raise HTTPException(status_code=404, detail="Products not found")

    return products
