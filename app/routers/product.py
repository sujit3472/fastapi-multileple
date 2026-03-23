import os
import shutil

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..database import get_db
from ..models.product import Product
from ..models.category import Category
from ..schemas.product import ProductCreate
from ..schemas.product import ProductUpdate
from ..schemas.product import ProductResponse

from ..utils.response import api_response
from ..utils.file_upload import save_image
from ..dependencies.auth import get_current_user


router = APIRouter(
    prefix="/products",
    tags=["Products"],
    dependencies=[Depends(get_current_user)]
)

UPLOAD_DIR = "uploads/products"

ALLOWED_TYPES = [
    "image/jpeg",
    "image/png",
    "image/jpg",
    "image/webp",
    "image/gif",
]

@router.post("/")
def create_product(
    name: str = Form(...),
    price: int = Form(...),
    category_id: int = Form(...),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    try:
        filename = save_image(image, "products")

    except ValueError as e:
        return api_response(400, str(e), None, False)

    product = Product(
        name=name,
        price=price,
        category_id=category_id,
        image=filename
    )

    try:
        db.add(product)
        db.commit()
        db.refresh(product)
    except IntegrityError as e:
        db.rollback()
        msg = str(e.orig).lower()
        if "foreign key" in msg:
            return api_response(400, "Invalid category id",None,False)

        if "duplicate" in msg:
            return api_response(400, "Duplicate Product name",None,False)

        return api_response(400, "Database error",None,False)
        
    return api_response(200, "Product Created", ProductResponse.model_validate(product).model_dump(), True)
    


@router.get("/")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    data = [
        ProductResponse.model_validate(p).model_dump()
        for p in products
    ]
    return api_response(200, "Product Lists", data, True)


@router.put("/{id}")
def update_product(
    id: int,
    name: str = Form(...),
    price: int = Form(...),
    category_id: int = Form(...),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    db_product = db.query(Product).filter(
        Product.id == id
    ).first()

    if not db_product:
        return api_response(404, "Product not found",None,False)
    
    try:
        filename = save_image(image, "products", db_product.image)

    except ValueError as e:
        return api_response(400, str(e), None, False)
    
    db_product.name = name
    db_product.price = price
    db_product.category_id = category_id
    db_product.image = filename

    try:
        db.commit()
        db.refresh(db_product)
    
    except IntegrityError as e:
        db.rollback()

        msg = str(e.orig).lower()

        if "foreign key" in msg:
            return api_response(400, "Invalid category id",None,False)

        if "duplicate" in msg:
            return api_response(400, "Duplicate value",None,False)

        return api_response(400, "Database error",None,False)

    return api_response(200, "Product Updated successfully", ProductResponse.model_validate(db_product).model_dump(), True)



@router.delete("/{id}")
def delete_product(id:int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(
        Product.id == id
    ).first()
    
    if not db_product:
        return api_response(404, "Product not found", None, False)
    
    try:
        db.delete(db_product)
        db.commit()
    except IntegrityError as e:
        db.rollback()

        msg = str(e.orig).lower()

        if "foreign key" in msg:
            return api_response(400, "Invalid category id", None, False)

        if "duplicate" in msg:
            return api_response(400, "Duplicate value", None, False)

        return api_response(400, "Database error", None, False)


    return api_response(200, "Product deleted successfully", None, True)