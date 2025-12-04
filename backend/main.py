"""
FastAPI main application
UFC Analytics API Backend
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from api import fighters, predictions
from database.config import get_db
from database.schema import User

app = FastAPI(
    title="UFC Analytics API",
    description="API for UFC fight statistics, predictions, and betting analysis",
    version="1.0.0"
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer(auto_error=False)

# Include routers
app.include_router(fighters.router, prefix="/api/v1")
app.include_router(predictions.router, prefix="/api/v1")


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "UFC Analytics API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "operational"
    }


@app.get("/api/v1/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/api/v1/stats")
def get_api_stats(db: Session = Depends(get_db)):
    """Get API statistics"""
    from database.schema import Fighter, Fight

    total_fighters = db.query(Fighter).count()
    total_fights = db.query(Fight).count()

    return {
        "total_fighters": total_fighters,
        "total_fights": total_fights,
        "features": {
            "fighter_search": True,
            "fight_predictions": True,
            "betting_analysis": True,
            "head_to_head": True
        }
    }


# Middleware for rate limiting and usage tracking
@app.middleware("http")
async def track_usage(request, call_next):
    """Track API usage for free tier limits"""
    # TODO: Implement rate limiting for non-premium users
    response = await call_next(request)
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
