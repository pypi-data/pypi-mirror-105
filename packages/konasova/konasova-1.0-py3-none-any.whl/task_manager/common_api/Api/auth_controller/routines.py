from fastapi.responses import JSONResponse
from .dataclases import ErrorResponse, Error


def get_error_response(text: str):
    return ErrorResponse(error=Error(text=text)).dict()

def JSONErrorResponse(status_code: int, text: str):
    return JSONResponse(status_code=status_code, content=get_error_response(text=text))