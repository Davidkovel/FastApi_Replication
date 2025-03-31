import os
import pathlib

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DATABASE: str

    class Config:
        # f"{pathlib.Path(__file__).resolve().parent.parent.parent}/.env"
        env_file = f"app/config/.env"


Config = Settings()
