"""
API v1 router configuration
"""

from fastapi import APIRouter
from app.api.api_v1.endpoints import auth, users, clients, financial, compliance, ai

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(clients.router, prefix="/clients", tags=["clients"])
api_router.include_router(financial.router, prefix="/financial", tags=["financial"])
api_router.include_router(compliance.router, prefix="/compliance", tags=["compliance"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
