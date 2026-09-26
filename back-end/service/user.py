from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, Response, Request
from model import User
from sqlalchemy.exc import IntegrityError
from schema.user import user_create, user_login, user_update
from passlib.context import CryptContext
import time
from datetime import datetime, timedelta, timezone
from core.config import settings
from jose import jwt
from model.role import Role
from service.menu_item_service import MenuItemService 
password_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


def get_all(session: Session):
    return session.execute(select(User).options(joinedload(User.role)).order_by(User.created_at)).scalars().all()

def get_one(id: int,session: Session):
    user = session.get(User, id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")
    
    return user

def _current_user_id(session: Session, current_user_id: int | None = None) -> int | None:
    if current_user_id is not None:
        return current_user_id
    return session.info.get("current_user_id")


def create(data: user_create, session: Session, current_role_id: int | None = None):
    try:
        exist_user = session.execute(select(User).where(User.email == data.email)).scalars().first()
        if exist_user: 
            raise HTTPException(status_code=400, detail="Username or email already exists")

        role = session.execute(select(Role).select(Role.id)).first()
        print(f"Role id {role}")
        roleId = None
        if current_role_id is None and role:
            roleId = role

        roleId = data.role_id
        
        user = User(
            username = data.username,
            email = data.email,
            password = hash_password(data.password),
            status= data.status,
            role_id = roleId
        )
        
        
        session.add(user)
        session.commit()
        session.refresh(user)
        
        return { 'message': 'Success', 'data': user }
    except HTTPException:
        session.rollback()
        raise
    except IntegrityError as e:
        session.rollback()
       
        raise HTTPException(status_code=400, detail=f"DB IntegrityError: {str(e.orig)}")

    except Exception as e:
        session.rollback()
       
        raise HTTPException(status_code=500, detail=f"Unexpected error: {repr(e)}")
    
def update(id: int, data: user_update, session: Session, current_user_id: int | None = None):
    try:
        user = session.get(User, id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found!")
        
        user.username = data.username
        user.email = data.email
        
        user.status = data.status
        user.role_id = data.role_id

        if data.password:
            user.password = hash_password(data.password)

        audit_user_id = _current_user_id(session, current_user_id)
        if audit_user_id is not None:
            user.updated_by = audit_user_id
        
        session.add(user)
        session.commit()
        session.refresh(user)
        return { "message": "Success", "data": user }
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def delete(id: int, session: Session):
    try:
        user = session.get(User, id)
        if not user:
            raise HTTPException(status_code=404, detail='User not found!')
        
        session.delete(user)
        session.commit()
        return { "message": "Success", "data": user }
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
def delete_many(ids: list[int], session: Session):
    
    try:
        users = session.execute(select(User).where(User.id.in_(ids))).scalars().all()
        
        if not users:
            raise HTTPException(status_code=404, detail="User not found!")
        
        for user in users:
            session.delete(user)
        
        session.commit()
        return {"message": "Success"}
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
async def login(data: user_login,request: Request ,response: Response, session: Session):

    try:
        user = session.execute(
            select(User).where(
                User.email == data.email,
                User.status.is_(True),
            )
        ).scalars().first()
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        verify_pass = verify_password(data.password, user.password)
        
        if not verify_pass:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        

        expire_time = datetime.now(timezone.utc) + timedelta(days=1)
        token = create_token(sub= data.email)
        
        menu_id = []
        if user.role.status:
            menu_id = list(user.get_menu_ids())

        menu_payload = []
        menu_all_payload = []
        try:
            menu_payload = await MenuItemService(session).get_menu_by_id(menu_id)
            menu_all_payload = await MenuItemService(session).get_all_menu_by_id(menu_id)
        except Exception:
            menu_payload = []
            menu_all_payload = []


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
        
        payload = {"message": "Success", "user": user.to_dict(), "token": token, "menu": menu_payload, "menu_all": menu_all_payload }

        return payload
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Login failed: " + str(e))

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


    
