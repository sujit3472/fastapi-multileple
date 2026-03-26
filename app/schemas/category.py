from typing import List

from pydantic import BaseModel

from app.schemas.product import ProductResponse


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id : int
    name: str
    products: List[ProductResponse]
    
    class Config:
        orm_mode = True
        from_attributes = True


class CategoryUpdate(BaseModel):
    name: str