import fastapi

from routers.router import router


app = fastapi.FastAPI()
app.include_router(router)
