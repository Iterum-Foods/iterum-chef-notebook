from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from typing import Union
import logging
import traceback

logger = logging.getLogger(__name__)

class AppError(Exception):
    """Base application error class"""
    def __init__(self, message: str, status_code: int = 500, error_code: str = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)

class ValidationError(AppError):
    """Validation error"""
    def __init__(self, message: str, error_code: str = "VALIDATION_ERROR"):
        super().__init__(message, 400, error_code)

class NotFoundError(AppError):
    """Resource not found error"""
    def __init__(self, message: str, error_code: str = "NOT_FOUND"):
        super().__init__(message, 404, error_code)

class UnauthorizedError(AppError):
    """Unauthorized access error"""
    def __init__(self, message: str, error_code: str = "UNAUTHORIZED"):
        super().__init__(message, 401, error_code)

class ForbiddenError(AppError):
    """Forbidden access error"""
    def __init__(self, message: str, error_code: str = "FORBIDDEN"):
        super().__init__(message, 403, error_code)

async def error_handler_middleware(request: Request, call_next):
    """Global error handling middleware"""
    try:
        response = await call_next(request)
        return response
    except AppError as e:
        # Handle application-specific errors
        logger.error(f"Application error: {e.message}", extra={
            "error_code": e.error_code,
            "status_code": e.status_code,
            "path": request.url.path
        })
        
        return JSONResponse(
            status_code=e.status_code,
            content={
                "error": True,
                "message": e.message,
                "error_code": e.error_code,
                "status_code": e.status_code
            }
        )
    except HTTPException as e:
        # Handle FastAPI HTTP exceptions
        logger.error(f"HTTP error: {e.detail}", extra={
            "status_code": e.status_code,
            "path": request.url.path
        })
        
        return JSONResponse(
            status_code=e.status_code,
            content={
                "error": True,
                "message": e.detail,
                "error_code": "HTTP_ERROR",
                "status_code": e.status_code
            }
        )
    except SQLAlchemyError as e:
        # Handle database errors
        logger.error(f"Database error: {str(e)}", extra={
            "path": request.url.path,
            "traceback": traceback.format_exc()
        })
        
        return JSONResponse(
            status_code=500,
            content={
                "error": True,
                "message": "Database error occurred",
                "error_code": "DATABASE_ERROR",
                "status_code": 500
            }
        )
    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error: {str(e)}", extra={
            "path": request.url.path,
            "traceback": traceback.format_exc()
        })
        
        return JSONResponse(
            status_code=500,
            content={
                "error": True,
                "message": "An unexpected error occurred",
                "error_code": "INTERNAL_ERROR",
                "status_code": 500
            }
        )

def create_error_response(
    message: str,
    status_code: int = 500,
    error_code: str = None,
    details: dict = None
) -> dict:
    """Create a standardized error response"""
    response = {
        "error": True,
        "message": message,
        "status_code": status_code
    }
    
    if error_code:
        response["error_code"] = error_code
    
    if details:
        response["details"] = details
    
    return response

def create_success_response(
    data: Union[dict, list],
    message: str = "Success",
    status_code: int = 200
) -> dict:
    """Create a standardized success response"""
    return {
        "error": False,
        "message": message,
        "status_code": status_code,
        "data": data
    } 