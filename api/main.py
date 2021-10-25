from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from api.utils.db_util import database
from api.auth import router as auth_router
from api.users import router as user_router

from api.exceptions.business import BusinessException


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

@app.exception_handler(BusinessException)
async def unicorn_exception_handler(request: Request, e: BusinessException):
    return JSONResponse(
        status_code=e.status_code,
        content={"status_code":e.status_code, 'message': e.detail}
    )


app.include_router(auth_router.router, tags=['Auth'])
app.include_router(user_router.router, tags=['Users'])
