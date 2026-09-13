from fastapi import Depends, APIRouter, Request, Form, File, UploadFile
from sqlalchemy.orm import Session
from infrastructure.database import get_session
from schema.product import Product, ProductRead
from redis.asyncio import Redis
from service.product import get_all_product, create_product, update_product, delete_product
from infrastructure.redis import get_redis_from_request
import json
from core.dependency import get_current_user, require_menu
from model.user import User

router = APIRouter(prefix="/product", dependencies=[Depends(require_menu('/product'))])

@router.get('/')
async def get_all(session: Session = Depends(get_session), redis: Redis = Depends(get_redis_from_request)):
    cache_key = "products:all"
    if redis is not None:
        try:
            cached = await redis.get(cache_key)
            if cached:
                print(f"Cache Data >>>>>>>>>>>>")
                return json.loads(cached)
        except Exception:
            pass

    data = get_all_product(session)
    if redis is not None:
        try:
            await redis.set(cache_key, json.dumps(data, default=str), ex=900)
            print(f"Data from database >>>>> ")
        except Exception:
            pass

    return data

@router.post('/create')
async def create(
    code: str = Form(...),
    name: str = Form(...),
    description: str | None = Form(None),
    expire_date: str | None = Form(None),
    package: str | None = Form(None),
    stock: int | None = Form(None),
    category_id: int = Form(...),
    measurement_id: int | None = Form(None),
    review: int | None = Form(None),
    images: list[UploadFile] | None = File(None),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    redis: Redis = Depends(get_redis_from_request)
):
    data = Product(
        code=code,
        name=name,
        description=description,
        expire_date=expire_date,
        package=package,
        stock=stock,
        category_id=category_id,
        review=review,
        images=images,
        measurement_id=measurement_id
    )
    print(f"Product data >>>>>>>>>>{data}")
    result = create_product(data, session, current_user.id)
    if redis is not None:
        try:
            await redis.delete("products:all")
        except Exception:
            pass
    return result

@router.post('/update/{id}')
async def update(
    id: int,
    code: str = Form(...),
    name: str = Form(...),
    description: str | None = Form(None),
    expire_date: str | None = Form(None),
    package: str | None = Form(None),
    stock: int | None = Form(None),
    category_id: int = Form(...),
    measurement_id: int | None = Form(None),
    review: int | None = Form(None),
    images: list[UploadFile] | None = File(None),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    redis: Redis = Depends(get_redis_from_request)
):
    data = Product(
        code=code,
        name=name,
        description=description,
        expire_date=expire_date,
        package=package,
        stock=stock,
        category_id=category_id,
        review=review,
        images=images,
        measurement_id=measurement_id
    )
    print(f"Product data >>>>>>>>>>>> {data}")
    result = update_product(id, data, session, current_user.id)
    if redis is not None:
        try:
            await redis.delete("products:all")
        except Exception:
            pass
    return result

@router.delete('/delete')
async def delete(id: list[int], session: Session = Depends(get_session), redis: Redis = Depends(get_redis_from_request)):
    result = delete_product(id, session)
    if redis is not None:
        try:
            await redis.delete("products:all")
        except Exception:
            pass
    return result
