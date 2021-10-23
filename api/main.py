from fastapi import FastAPI
from api.utils.db_util import database


app = FastAPI(
    docs_url="/docs",
    redoc_url="/redocs",
    title="/FastAPI (python)",
    description="FastAPI Framework, high performance, <br> "
    "easy to learn, fast to code, ready for production",
    version="1.0",
    openapi_url="/openapi.json",
)


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


@app.get("/hello")
def hello():
    return "hello world"
