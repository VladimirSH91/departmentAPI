from fastapi import APIRouter

from .department import department_router

router = APIRouter()

router.include_router(department_router)
