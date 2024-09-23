from fastapi import APIRouter

from app.api.endpoints.content_generation import content_generation_router
from app.api.endpoints.image_generation import image_generation_router
from app.api.endpoints.blog_generation import blog_generation_router
from app.api.endpoints.ad_generation import ad_generation_router
from app.api.endpoints.auto_content_generation import aut_content_generation_router
api_router = APIRouter()

api_router.include_router(content_generation_router, tags=["Content Generation"])
api_router.include_router(aut_content_generation_router,tags=["Auto Content Generation"])
api_router.include_router(image_generation_router,tags=["Image Generation"])
api_router.include_router(blog_generation_router,tags=["Blog Generation"])
api_router.include_router(ad_generation_router,tags=["Ad Generation"])