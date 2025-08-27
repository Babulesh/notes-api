from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = (
    "postgresql+asyncpg://notes_user:notes_pass@localhost:5433/notes_db"
    )
    JWT_SECRET: str = "devsecret"
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


class Config:
    env_file = ".env"


settings = Settings()