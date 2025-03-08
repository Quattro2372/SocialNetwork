from fastapi import FastAPI

from libs.handlers import user_service

app = FastAPI(title="API")
app.include_router(user_service.api_router)
