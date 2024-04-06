from fastapi import APIRouter

from routers import auth, users, goals, posts, search, subscriptions, likes, comments

router = APIRouter()

router.include_router(auth.router, prefix="", tags=["Auth"])
router.include_router(users.router, prefix="", tags=["User"])
router.include_router(goals.router, prefix="/goal", tags=["Goal"])
router.include_router(posts.router, prefix="/post", tags=["Post"])
router.include_router(search.router, prefix="/search", tags=["Search"])
router.include_router(subscriptions.router, tags=["Subscription"])
router.include_router(likes.router, tags=["Like"])
router.include_router(comments.router, tags=["Comment"])
