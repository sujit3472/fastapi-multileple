from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from .database import engine, Base

from .routers import product, category


app = FastAPI()

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "success": False,
            "message": exc.detail,
            "data": None,
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):

    return JSONResponse(
        status_code=500,
        content={
            "status": 500,
            "success": False,
            "message": str(exc),
            "data": None,
        },
    )

Base.metadata.create_all(bind=engine) # table created only when call this method

app.include_router(category.router)
app.include_router(product.router)