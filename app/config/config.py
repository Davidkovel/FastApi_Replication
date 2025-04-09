import os
import pathlib

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVER_ADDRESS: str = os.environ.get('SERVER_ADDRESS', '0.0.0.0:8080')
    SERVER_HOST: str = os.environ.get('SERVER_HOST', '0.0.0.0')
    SERVER_PORT: int = os.environ.get('SERVER_PORT', 8080)

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DATABASE: str

    RANDOM_SECRET: str = os.environ.get('RANDOM_SECRET', '')
    ALGORITHM: str = os.environ.get('ALGORITHM', '')

    ACCESS_TOKEN_EXPIRES_MINUTES: int = os.environ.get('ACCESS_TOKEN_EXPIRES_MINUTES', 0)
    ACCESS_TOKEN_EXPIRES_HOURS: int = os.environ.get('ACCESS_TOKEN_EXPIRES_HOURS', 12)
    ACCESS_TOKEN_EXPIRES_DAYS: int = os.environ.get('ACCESS_TOKEN_EXPIRES_DAYS', 0)

    class Config:
        # f"{pathlib.Path(__file__).resolve().parent.parent.parent}/.env"
        env_file = f"app/config/.env"


Config = Settings()
