from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    SQLITE3: str

    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }

@lru_cache()
def get_settings():
    return Settings()
