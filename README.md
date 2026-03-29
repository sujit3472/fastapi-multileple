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


## 10. File upload in fastAPI
    pip install python-multipart
    add the below lines

    from fastapi import FastAPI, Form

## 11. Authentication and authorization
    pip install python-jose passlib[bcrypt] python-multipart
    pip install pydantic[email]
    pip install bcrypt==4.0.1
    -create the respective auth files in each directory
    -register the route in main.py file


## For Migration use ##
## 1. Install package
    pip install alembic

## 2. Initialize Alembic (inside app folder) IMPORTANT: run where main.py exists
    alembic init alembic
 
## 3. Configure database URL
    Open app/alembic.ini
    Set DB
    sqlalchemy.url = mysql+pymysql://root:password@localhost/fastapi_db

## 4. Create DB Manually

## 5. Fix models import (IMPORTANT)
    from ..database import Base
    change to 
    from database import Base
    update this change inside the all models files
    app/models/user.py

## 6. Fix env.py (MOST IMPORTANT)
    Open 
        app/alembic/env.py
    Add at the top
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

    Then import models correctly:
        from database import Base
        from models.user import User
        from models.product import Product
        from models.category import Category

    Set metadata
        target_metadata = Base.metadata

## 7. Run migration (inside app folder)
    alembic revision --autogenerate -m "create tables"
    alembic upgrade head

## If you want to alter the table use the below steps

## 1. In model file add the fields you want
## 2. After that run the below command with the details
    alembic revision --autogenerate -m "add status and timestamps to users"
## 3. If you want to update the default value go to 
    op.add_column(
    "users",
    sa.Column("status", sa.Integer(), server_default="1")
    )
## 4. then run the below command
    alembic upgrade head


## To get the all installed packages using the below command for the project setup in other machine
    pip freeze > requirements.txt

## Removed Mysql DB connection and used postgres SQL 
    pip uninstall pymysql mysqlclient
    pip install psycopg2-binary