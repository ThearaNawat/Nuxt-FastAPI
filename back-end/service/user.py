from sqlmodel import select, Session
from fastapi import HTTPException, Response
from model import User
from sqlalchemy.exc import IntegrityError
from schema.user import user_create, user_login
from passlib.context import CryptContext
import time
from datetime import datetime, timedelta, timezone
from config import settings
from jose import jwt

password_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

def get_all(session: Session):
    return session.exec(select(User).order_by(User.id)).all()

def get_one(id: int,session: Session):
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")
    
    return user

def create(data: user_create, session: Session):
    try:
        exist_user = session.exec(select(User).where(User.email == data.email)).first()
        if exist_user: 
            raise HTTPException(400, "Username or email already exists")
        
        user = User(
            username = data.username,
            email = data.email,
            password = hash_password(data.password),
            status= data.status
        )
        
        session.add(user)
        session.commit()
        session.refresh(user)
        
        return { 'message': 'Success', 'data': user }
    except IntegrityError as e:
        session.rollback()
       
        raise HTTPException(status_code=400, detail=f"DB IntegrityError: {str(e.orig)}")

    except Exception as e:
        session.rollback()
       
        raise HTTPException(status_code=500, detail=f"Unexpected error: {repr(e)}")

def update(id: int, data: user_create, session: Session):
    try:
        user = session.get(User, id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found!")
        
        user.username = data.username
        user.email = data.email
        user.password = data.password
        user.status = data.status
        session.add(user)
        session.commit()
        session.refresh(user)
        return { "message": "Success", "data": user }
    except Exception:
        HTTPException(status_code=500, detail=Exception)    

def delete(id: int, session: Session):
    try:
        user = session.get(User, id)
        if not user:
            raise HTTPException(status_code=404, detail='User not found!')
        
        session.delete(user)
        session.commit()
        return { "message": "Success", "data": user }
    except Exception:
        raise HTTPException(status_code=500, detail=Exception)
    
def delete_many(ids: list[int], session: Session):
    
    try:
        users = session.exec(select(User).where(User.id.in_(ids))).all()
        
        if not users:
            raise HTTPException(status_code=404, detail="User not found!")
        
        for user in users:
            session.delete(user)
            
        session.commit()
        return {"message": "Success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
    
def login(data: user_login, response: Response, session: Session):
    try:
        
        user = session.exec(select(User).where(User.email == data.email and User.status == True)).first()
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        verify_pass = verify_password(data.password, user.password)
        
        if not verify_pass:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        expire_time = datetime.now(timezone.utc) + timedelta(days=1)
        token = create_token(sub= data.email)
        response.set_cookie(
            key="TOKEN", 
            value=token, 
            max_age= 60 * 60 * 24, 
            httponly=True, 
            samesite="lax", 
            secure=False,
            expires=expire_time,
            path="/"
        )
        
        return {"message": "Success", "user": user, "token": token}
    except Exception:
        session.rollback()
        raise HTTPException(500, "Login fail!")

def logout(response: Response):
    response.delete_cookie(
        key="TOKEN",
        samesite="lax",
        secure=False,
        httponly=True,
        path="/"
    )
    return {"message": "Logout success"}
    
def hash_password(password: str) -> str:
    return password_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)

def create_token(sub: str) -> str:
    expire = int(time.time()) + 60 * 60 * 24
    payload = {"sub": sub, "exp": expire, "type": "access"}
    return jwt.encode(payload,SECRET_KEY,ALGORITHM)


    