from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from routes.user import router as user_router
from routes.purchase import router as purchase_router
from routes.monthlybill import router as bill_router
from routes.settlement import router as settlement_router
from routes.room import router as room_router
from routes.chore import router as chore_router
from routes.notification import router as notification_router

os.makedirs("avatars", exist_ok=True)
app = FastAPI()
app.mount("/avatars", StaticFiles(directory="avatars"), name="avatars")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)
app.include_router(user_router)
app.include_router(purchase_router)
app.include_router(bill_router)
app.include_router(settlement_router)
app.include_router(room_router)
app.include_router(chore_router)
app.include_router(notification_router)
