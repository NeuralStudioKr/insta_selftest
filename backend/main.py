from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import webhook, comments, accounts, auth
from config import settings
import os

app = FastAPI(
    title="Instagram Comment Manager API",
    description="인스타그램 댓글 관리 API",
    version="1.0.0"
)

# Railway 배포를 위한 CORS 설정 (프론트엔드 URL을 환경 변수로 받을 수 있음)
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")

# CORS 설정
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    frontend_url,
]
# 환경 변수에서 추가 CORS 허용 URL이 있으면 추가
if os.getenv("ALLOWED_ORIGINS"):
    allowed_origins.extend(os.getenv("ALLOWED_ORIGINS").split(","))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터 디렉토리 생성
os.makedirs(settings.data_dir, exist_ok=True)

# 라우터 등록
app.include_router(webhook.router, tags=["webhook"])
app.include_router(comments.router, prefix="/api", tags=["comments"])
app.include_router(accounts.router, prefix="/api", tags=["accounts"])
app.include_router(auth.router, prefix="/api", tags=["auth"])


@app.get("/")
async def root():
    return {"message": "Instagram Comment Manager API", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
