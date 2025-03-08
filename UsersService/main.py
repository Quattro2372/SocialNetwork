from fastapi import FastAPI

from libs.handlers import auth, registration, getters, profile
from libs.database.queries.create_tables import create_tables

app = FastAPI(title="User Service")
app.include_router(registration.api_router)
app.include_router(auth.api_router)
app.include_router(profile.api_router)

app.include_router(getters.api_router)

create_tables()
