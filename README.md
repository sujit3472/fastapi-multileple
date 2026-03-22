# FastAPI Multiple File Project Setup Guide

## 1. Project Structure
    project-root/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── dependencies.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── product.py
│   │   └── category.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── product.py
│   │   └── category.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── product.py
│   │   └── category.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── response.py
│   └── myenv/

Each folder must contain **init**.py

## 2. Create Virtual Environment

cd /var/www/html/FastAPI-Demo/app python -m venv myenv source
myenv/bin/activate

## 3. Install Packages

pip install fastapi uvicorn sqlalchemy pymysql pydantic

## 4. Database Example

from sqlalchemy import create_engine from sqlalchemy.orm import
sessionmaker, declarative_base

DB_URL = "mysql+pymysql://root:password@localhost:3306/fast_api"

engine = create_engine(DB_URL)

SessionLocal = sessionmaker( autocommit=False, autoflush=False,
bind=engine )

Base = declarative_base()

## 5. Import Rules

main.py 
from .database import engine, Base 
from .routers import product

routers/product.py 
from ..database import get_db 
from ..models.product

import Product
models/product.py from ..database import Base

## 6. Deactivate conda

conda deactivate conda deactivate

## 7. Activate env

cd /var/www/html/FastAPI-Demo source app/myenv/bin/activate

## 8. Run project

python -m uvicorn app.main:app --reload

## 9. Swagger

http://127.0.0.1:8000/docs
