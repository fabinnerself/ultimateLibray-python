import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

# Import configurations and database
from .config import settings
from .database import get_database

# Import routers
from .routers import books, users

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI application without lifespan for Vercel compatibility
app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    description=settings.description,
    docs_url="/docs" if settings.environment == "development" else None,
    redoc_url="/redoc" if settings.environment == "development" else None,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "https://your-frontend-domain.vercel.app",  # Add your frontend domain
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.project_name}",
        "version": settings.version,
        "environment": settings.environment,
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.version}

# Include routers with API prefix
app.include_router(
    books.router,
    prefix=settings.api_v1_prefix,
    tags=["Books"]
)

app.include_router(
    users.router,
    prefix=settings.api_v1_prefix,
    tags=["Users & Authentication"]
)

# Global exception handler
@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    logger.error(f"Internal server error: {exc}")
    return HTTPException(
        status_code=500,
        detail="Internal server error"
    )

# For Vercel deployment
handler = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.environment == "development"
    )
