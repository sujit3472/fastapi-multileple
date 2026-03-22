from fastapi.responses import JSONResponse


def api_response(
    status: int,
    message: str,
    data=None,
    success: bool = True
):

    return JSONResponse(
        status_code=status,
        content={
            "status": status,
            "success": success,
            "message": message,
            "data": data,
        },
    )