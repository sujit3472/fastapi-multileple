from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..database import get_db
from ..models.category import Category
from ..schemas.category import CategoryCreate
from ..schemas.category import CategoryUpdate
from ..dependencies.auth import get_current_user

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
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


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

    