from fastapi import FastAPI
from app.core.config import settings
from app.core.database import database
from app.models import users

app = FastAPI(title=settings.project_name)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def root():
    return {"message": f"API запущено успешно в режиме {settings.env}"}

@app.get("/users/")
async def get_users():
    query = users.select()
    return await database.fetch_all(query)
