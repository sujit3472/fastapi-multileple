from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.category import Category
from ..schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from ..dependencies.auth import get_current_user
from app.utils.response import api_response

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
    dependencies=[Depends(get_current_user)]
)


@router.post("/")
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Category).filter(
        Category.name == data.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Category already exists"
        )

    category = Category(name=data.name)

    db.add(category)
    db.commit()
    db.refresh(category)

    return category



@router.get("/")
def get_categories(
    search: str = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)):

    query = db.query(Category)

    # Search filter
    if search:
        query = query.filter(Category.name.ilike(f"%{search}%"))

     # Total count (before pagination)
    total = query.count()

    # Pagination
    offset = (page - 1) * limit
    categoryList = query.offset(offset).limit(limit).all()

    data = [
        CategoryResponse.model_validate(c).model_dump()
        for c in categoryList
    ]

    return api_response(200, "Category Lists", {
        "items": data,
        "total": total,
        "page": page,
        "limit": limit
    }, True)


@router.get("/{id}")
def get_category_details(
    id: int, 
    db: Session = Depends(get_db)):
    
    db_category = db.query(Category).filter(Category.id == id).first()

    if not db_category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )
    
    return api_response(200, "Category Details", CategoryResponse.model_validate(db_category).model_dump(), True)



@router.put("/{id}")
def update_category(
    id: int,
    data: CategoryUpdate,
    db: Session = Depends(get_db)
):

    db_category = db.query(Category).filter(
        Category.id == id
    ).first()

    if not db_category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    db_category.name = data.name

    try:
        db.commit()
        db.refresh(db_category)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Category name already exists"
        )

    return db_category


@router.delete("/{id}")
def delete_category(
    id: int,
    db: Session = Depends(get_db)
):

    db_category = db.query(Category).filter(
        Category.id == id
    ).first()

    if not db_category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    try:
        db.delete(db_category)
        db.commit()

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Category cannot be deleted (used in products)"
        )

    return {
        "message": "Category deleted successfully"
    }

    