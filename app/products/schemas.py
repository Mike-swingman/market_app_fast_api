from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProductSchema(BaseModel):
    name: str
    description: str
    price: int
    quantity: int
    category_id: int

    model_config = ConfigDict(from_attributes=True)


class ProductUpdateSchema(BaseModel):
    price: int
    quantity: int


class ProductFilterSchema(BaseModel):
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    min_quantity: Optional[int] = None
    name_pattern: Optional[str] = None
    category_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
