@echo off
REM 로컬 개발 환경 시작 스크립트 (Windows)

echo 🚀 Instagram 댓글 관리 시스템 로컬 실행
echo ========================================

REM 백엔드 실행
echo.
echo 📦 백엔드 시작 중...
cd backend

REM 가상환경 확인 및 생성
if not exist "venv" (
    echo 가상환경 생성 중...
    python -m venv venv
)

REM 가상환경 활성화
call venv\Scripts\activate.bat

REM 의존성 설치
if not exist ".deps_installed" (
    echo 의존성 설치 중...
    pip install -r requirements.txt
    type nul > .deps_installed
)

REM .env 파일 확인
if not exist ".env" (
    echo ⚠️  .env 파일이 없습니다!
    echo backend\.env 파일을 생성하고 다음 변수들을 설정하세요:
    echo   - INSTAGRAM_ACCESS_TOKEN
    echo   - INSTAGRAM_APP_SECRET
    echo   - WEBHOOK_VERIFY_TOKEN
    echo   - API_BASE_URL=http://localhost:8000
    pause
    exit /b 1
)

echo ✅ 백엔드 서버 시작 (포트 8000)
echo    API 문서: http://localhost:8000/docs
start "Backend Server" cmd /k "uvicorn main:app --reload --port 8000"

cd ..

REM 프론트엔드 실행
echo.
echo 📦 프론트엔드 시작 중...
cd frontend

REM 의존성 확인
if not exist "node_modules" (
    echo 의존성 설치 중...
    call npm install
)

REM .env.local 파일 확인
if not exist ".env.local" (
    echo ⚠️  .env.local 파일이 없습니다!
    echo frontend\.env.local 파일을 생성하고 다음을 설정하세요:
    echo   NEXT_PUBLIC_API_URL=http://localhost:8000
    pause
    exit /b 1
)

echo ✅ 프론트엔드 서버 시작 (포트 3000)
echo    웹사이트: http://localhost:3000
start "Frontend Server" cmd /k "npm run dev"

cd ..

echo.
echo ========================================
echo ✅ 서버가 실행 중입니다!
echo.
echo 백엔드: http://localhost:8000
echo 프론트엔드: http://localhost:3000
echo API 문서: http://localhost:8000/docs
echo.
echo 각 서버 창을 닫으면 종료됩니다.
echo ========================================
pause
