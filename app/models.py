from sqlalchemy import Table, Column, Integer, String, ForeignKey
from app.core.database import metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True, index=True),
)
