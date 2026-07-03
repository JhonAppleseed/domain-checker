from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from backend.api import scan

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:8000",
    "http://localhost:8001"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(scan.router)