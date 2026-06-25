from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.router import router as api_router
from utils.logger import logger

app = FastAPI(
    title="Peek AI API",
    description="Screenshot intelligence engine built as an academic portfolio backend.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "app": "Peek AI Backend Engine",
        "version": "1.0.0",
        "docs_url": "/docs"
    }

logger.info("FastAPI Peek AI server loaded and configured successfully.")
