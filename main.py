import fastapi

from routers.router import router

from services.mailer import mailer


app = fastapi.FastAPI()
app.include_router(router)

@app.get("/")
def hello(mail = mailer.Mailer()):
    mail.send_email("Andrew.Klevcov@gmail.com", "123")

    return "hello"
