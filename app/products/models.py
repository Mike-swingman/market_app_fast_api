from fastapi import HTTPException
from sqlalchemy import ForeignKey, String, select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from sqlalchemy.ext.asyncio import AsyncSession
from app.products.schemas import ProductFilterSchema


class ProductCategory(Base):
    __tablename__ = "product_category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str]

    products: Mapped[list["Product"]] = relationship(back_populates="category")


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    quantity: Mapped[int]
    description: Mapped[str]
    category_id: Mapped[int] = mapped_column(
        ForeignKey("product_category.id"), nullable=False
    )

    category: Mapped[ProductCategory] = relationship(back_populates="products")

    @staticmethod
    async def filter_products(session: AsyncSession, filters: ProductFilterSchema):
        query = select(Product)

        # Фильтрация по цене
        if filters.min_price is not None:
            query = query.filter(Product.price >= filters.min_price)
        if filters.max_price is not None:
            query = query.filter(Product.price <= filters.max_price)

        # Фильтрация по количеству
        if filters.min_quantity is not None:
            query = query.filter(Product.quantity >= filters.min_quantity)

        # Фильтрация по имени
        if filters.name_pattern is not None:
            query = query.filter(Product.name.ilike(f"%{filters.name_pattern}%"))

        # Фильтрация по категории
        if filters.category_id is not None:
            query = query.filter(Product.category_id == filters.category_id)

        result = await session.execute(query)
        products = result.scalars().all()
        return products

    @staticmethod
    async def update_product(product_id, data, session: AsyncSession):

        query = select(Product).filter(Product.id == product_id)
        result = await session.execute(query)
        product = result.scalars().first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if data.price:
            product.price = data.price
        if data.quantity:
            product.quantity = data.quantity

        await session.commit()
        return {"message": "Product updated successfully"}

    @staticmethod
    async def delete(session, **filter_by):
        try:
            query = delete(Product).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()
            return {'status': 204, 'message': 'Deleted successfully'}
        except SQLAlchemyError:
            await session.rollback()
            raise Exception("Database Exc: Cannot insert data into table")
        except Exception:
            await session.rollback()
            raise Exception("Unknown Exc: Cannot insert data into table")