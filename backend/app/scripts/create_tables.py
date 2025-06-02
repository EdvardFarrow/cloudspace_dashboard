import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app.core.database import Base, engine
from sqlalchemy import create_engine
from app.auth import models 

engine = create_engine("postgresql+psycopg2://postgres:1@localhost:5432/cloudspace_dashboard")

def create_all_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Все таблицы успешно созданы.")

if __name__ == "__main__":
    create_all_tables()