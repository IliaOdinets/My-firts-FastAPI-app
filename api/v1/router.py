from fastapi import APIRouter
from api.v1.endpoints import notes, auth

api_router = APIRouter()
api_router.include_router(notes.router)
api_router.include_router(auth.router)