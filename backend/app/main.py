from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger

from app.core.config import get_settings
from app.core.security import setup_security
from app.core.logging import setup_logging
from app.api import auth, chat, system, pentest

# Initialize settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="Windows Server Assistant",
    description="Intelligent assistant for Windows Server management and penetration testing",
    version="1.0.0"
)

# Setup middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup logging
setup_logging()

# Setup security
setup_security(app)

# Include API routers under /api prefix
app.include_router(auth.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(system.router, prefix="/api")
app.include_router(pentest.router, prefix="/api")

# Mount static files
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "running",
        "version": "1.0.0"
    }
