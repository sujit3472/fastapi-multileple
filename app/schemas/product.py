from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    price: float
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    name : str
    price : float
    category_id : int

    class Config:
        orm_mode = True
        from_attributes = True

class ProductUpdate(BaseModel):
    name: str
    price: float
    category_id: int
