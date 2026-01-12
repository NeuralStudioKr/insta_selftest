from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """애플리케이션 설정"""
    instagram_access_token: str
    instagram_app_secret: str
    webhook_verify_token: str
    api_base_url: str = "http://localhost:8000"
    
    # OAuth 설정
    instagram_app_id: Optional[str] = None
    oauth_redirect_uri: str = "http://localhost:8000/api/auth/instagram/callback"
    
    # 데이터 저장 경로
    data_dir: str = "data"
    comments_file: str = "comments.json"
    
    # Railway 배포용 포트 (환경 변수에서 가져오거나 기본값 사용)
    port: int = 8000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
