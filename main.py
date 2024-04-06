import fastapi
from fastapi.middleware.cors import CORSMiddleware

from routers.router import router


app = fastapi.FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins = ["*"],
  allow_methods = ["*"],
  allow_headers = ["*"]
)

app.include_router(router)


@app.get("/")
def hello():

    return {"status": "ok"}
