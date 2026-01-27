
from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from database import create_db_and_table
from routers import user as user_router, category, supplier, product
from bots.chatbot import webhook
from utils.auth import auth_middleware
from utils.websocket import websocket_manager
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from contextlib import asynccontextmanager
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_table()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(user_router.router)
app.include_router(category.router)
app.include_router(supplier.router)
app.include_router(product.router)
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

@app.post("/webhook")
async def webhookchat(request: Request):
    return await webhook(request)

@app.websocket("/linebot")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket_manager.broadcast({"message": data})
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)

@app.get("/")
def read_root():
    return {"OK": True}