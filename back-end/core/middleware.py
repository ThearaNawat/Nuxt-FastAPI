
import logging
from fastapi import Request
from fastapi.responses import JSONResponse
logger = logging.getLogger(__name__)

from jose import jwt, JWTError
from sqlalchemy import select

from core.auth_utils import extract_token
from infrastructure.database import SessionLocal
from model.user import User  
from core.config import settings 

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


PUBLIC_PATHS = {
    "/",
    "/docs",
    "/openapi.json",
    "/redoc",
    "/user/login",
    "/user/create",
}

async def auth_middleware(request: Request, call_next):
    path = request.url.path

    if path in PUBLIC_PATHS:
        return await call_next(request)

    token = extract_token(request)
    if not token:
        return JSONResponse(
            {"detail": "Authorization token missing"},
            status_code=401,
        )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        email = payload.get("sub")
        
        if not email:
            return JSONResponse(
                {"detail": "Invalid token payload"},
                status_code=401,
            )
    except JWTError:
        return JSONResponse(
            {"detail": "Invalid or expired token"},
            status_code=401,
        )

    with SessionLocal() as session:
        user = session.execute(
            select(User).where(User.email == email, User.status.is_(True))
        ).scalars().first()

    if not user:
        return JSONResponse(
            {"detail": "User not found"},
            status_code=401,
        )

    if not user.status:
        return JSONResponse(
            {"detail": "User is inactive"},
            status_code=403,
        )


    request.state.user = user
    request.state.user_id = user.id

    return await call_next(request)


class ErrorHandlingMiddleware:
    """Middleware for global error handling."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            logger.error(f"Unhandled exception: {exc}")
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": "Internal server error",
                    "errors": [str(exc)],
                },
            )


class LoggingMiddleware:
    """Middleware for request/response logging."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, request: Request, call_next):
        logger.info(f"{request.method} {request.url.path}")
        response = await call_next(request)
        logger.info(f"Response status: {response.status_code}")
        return response
