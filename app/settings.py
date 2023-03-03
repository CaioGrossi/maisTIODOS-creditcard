# config.py
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    cryptography_key: str
    basic_auth_hash: str

    class Config:
        env_file = ".env"


settings = Settings()
