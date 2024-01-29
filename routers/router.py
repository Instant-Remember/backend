from fastapi import APIRouter

from routers import auth, users, goals, posts

router = APIRouter()

router.include_router(auth.router, prefix="", tags=["Auth"])
router.include_router(users.router, prefix="", tags=["User"])
router.include_router(goals.router, prefix="/goal", tags=["Goal"])
router.include_router(posts.router, prefix="/post", tags=['Post'])