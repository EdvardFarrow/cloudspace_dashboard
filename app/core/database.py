from databases import Database
from sqlalchemy import create_engine, MetaData

from app.core.config import settings  

database = Database(settings.DATABASE_URL)
engine = create_engine(settings.DATABASE_URL.replace('asyncpg', 'psycopg2'))  
metadata = MetaData()
