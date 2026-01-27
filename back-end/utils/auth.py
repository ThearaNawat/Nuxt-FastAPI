from fastapi import Request
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from sqlmodel import Session, select

from database import engine
from model.user import User  # adjust import if needed
from config import settings  # or where SECRET_KEY lives

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

PUBLIC_PATHS = {
    "/",
    "/docs",
    "/openapi.json",
    "/redoc",
    "/user/login",
    "/user/create",
    "/webhook",
}

async def auth_middleware(request: Request, call_next):
    path = request.url.path

    if path in PUBLIC_PATHS:
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return JSONResponse(
            {"detail": "Authorization header missing"},
            status_code=401,
        )

    if not auth_header.startswith("Bearer "):
        return JSONResponse(
            {"detail": "Invalid authorization format"},
            status_code=401,
        )

    token = auth_header.split(" ", 1)[1]
    
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

    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.email == email)
        ).first()

    if not user:
        return JSONResponse(
            {"detail": "User not found"},
            status_code=401,
        )


    request.state.user = user

    return await call_next(request)
