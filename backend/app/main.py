import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from app.core.config import settings
from app.core.database import database
from app.auth.models import User
from app.auth.routes import router as auth_router
import uvicorn


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

app = FastAPI(title=settings.project_name)

app.include_router(auth_router)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def root():
    return {"message": f"API запущено успешно в режиме {settings.env}"}

from sqlalchemy import select
from app.core.database import database
from app.auth.models import User

@app.get("/users/")
async def get_users():
    query = select(User)
    return await database.fetch_all(query)
