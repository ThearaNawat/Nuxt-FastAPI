
from fastapi import FastAPI, status, Depends
from fastapi.responses import JSONResponse
from infrastructure.database import create_db_and_table
from routers import user as user_router, category, supplier, product, menu_item_router, role_router, stock, stock_transaction, sales_order, customer, warehouse, purchase_order, purchase_order_item, measurement_router, currency, income, expense
from routers import invoice as invoice_router
from core.middleware import auth_middleware
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from core.config import settings
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from core.rate_limit import limiter
load_dotenv()
from infrastructure.redis import init_redis, close_redis



@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_table()
    redis_client = await init_redis()
    app.state.redis = redis_client
    try:
        yield
    finally:
        await redis_client.close()

app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter
app.middleware("http")(auth_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router.router)
app.include_router(category.router)
app.include_router(supplier.router)
app.include_router(product.router)
app.include_router(menu_item_router.menu_router)
app.include_router(role_router.role_router)
app.include_router(stock.router)
app.include_router(stock_transaction.router)
app.include_router(sales_order.router)
app.include_router(customer.router)
app.include_router(warehouse.router)
app.include_router(purchase_order.router)
app.include_router(purchase_order_item.router)
app.include_router(invoice_router.router)
app.include_router(measurement_router.router)
app.include_router(currency.router)
app.include_router(income.router)
app.include_router(expense.router)
app.include_router(__import__('routers.purchase_order', fromlist=['router']).router)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exec):
    return _rate_limit_exceeded_handler(request, exec)

@app.exception_handler(ValueError)
async def value_error_handler(request, exc: ValueError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "success": False,
            "message": str(exc),
            "errors": [str(exc)]
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "An unexpected error occurred",
            "errors": [str(exc)] if settings.DEBUG else ["Internal Server Error"]
        }
    )


@app.get("/")
def read_root():
    return {"OK": True}
