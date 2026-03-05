from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache

class Settings(BaseSettings):
    # Application settings
    app_name: str = "AI Smart Search Engine"
    debug: bool = False
    TAVILY_API_KEY : str =Field(...)
    GEMINI_API_KEY : str =Field(...)

    # Environment variable settings
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()
