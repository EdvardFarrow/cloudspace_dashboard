from app.models.users import metadata
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:1@localhost:5432/cloudspace_dashboard")

metadata.create_all(engine)