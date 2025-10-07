import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    应用配置类 (v3.1 - 增加密钥支持)
    """
    SEARCH_SH_COOKIE: Optional[str] = ""
    PORT: int = 8000
    NGINX_PORT: int = 8080
    # 新增：读取主密钥
    API_MASTER_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()

if not settings.SEARCH_SH_COOKIE:
    raise ValueError("SEARCH_SH_COOKIE is not set in the .env file. Please obtain it from your browser.")
