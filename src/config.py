from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class BaseConfig(BaseSettings):
    MONGO_URI: Optional[str]
    MONGO_DATABASE: Optional[str]
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")