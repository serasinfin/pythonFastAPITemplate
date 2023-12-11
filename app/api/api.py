# FastAPI imports
from fastapi import APIRouter

# App routers
from app.api.routers import hello
from app.api.routers import auth
from app.api.routers import user
from app.api.routers import user_roles
from app.api.routers import user_ability

api_router = APIRouter()

# Include routers
api_router.include_router(hello.router, prefix="/hello", tags=["Hello"])
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(user_roles.router, prefix="/user-roles", tags=["User Roles"])
api_router.include_router(user_ability.router, prefix="/user-abilities", tags=["User Abilities"])
