import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, field_validator, ValidationInfo, computed_field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode='before')
    def assemble_cors_origins(cls, v: Union[str, List[str]], info: ValidationInfo) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v

    POSTGRES_SERVER: str = "db"
    POSTGRES_USER: str = "testuser"
    POSTGRES_PASSWORD: str = "000000"
    POSTGRES_DB: str = "MyLibrary2"
    
    # 直接定义连接字符串，避免任何复杂处理
    SQLALCHEMY_DATABASE_URI: Optional[str] = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/MyLibrary2"

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()