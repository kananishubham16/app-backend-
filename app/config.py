import os
from pydantic import BaseModel

class Settings(BaseModel):
    APP_NAME: str = "Learning Setu API"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/learning_setu.db")
    CORS_ORIGINS: list[str] = ["*"]

settings = Settings()
