from fastapi import APIRouter

router = APIRouter(tags=["Base"])


@router.get("/")
async def root():
    return {
        "message": "Welcome to the AI Career Agent API",
        "docs": "/docs",
        "status": "online",
    }


@router.get("/health")
async def health_check():
    return {"status": "healthy"}
