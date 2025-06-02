from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

load_dotenv() 

class Settings(BaseSettings):
    env: str = "dev"
    project_name: str = "Catering Dashboard API"
    debug: bool = True
    DATABASE_URL: str
    SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()