from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    env: str = "dev"
    project_name: str = "Catering Dashboard API"
    debug: bool = True
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()