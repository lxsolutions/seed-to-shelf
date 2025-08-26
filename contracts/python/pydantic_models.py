






from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class Ingredient(BaseModel):
    name: str
    lot_id: UUID
    quantity: int = Field(..., description="Quantity in units")


class LotBase(BaseModel):
    product_code: str = Field(..., description="Product code (GS1-like)")
    quantity: Optional[int] = Field(None, description="Quantity in units")
    created_at: Optional[datetime] = None


class LotCreate(LotBase):
    pass


class LotUpdate(LotBase):
    lot_id: UUID
    updated_at: datetime


class ReadyMeal(BaseModel):
    product_id: UUID
    name: str
    sku: str = Field(..., description="Stock keeping unit (GS1-like)")
    ingredients: List[Ingredient]
    price: float


class OrderStatusChange(BaseModel):
    order_id: UUID
    status: str = Field(
        ...,
        pattern="^(PENDING|PREPARING|READY|DELIVERED|CANCELLED)$",
        description="Order status"
    )
    timestamp: datetime





