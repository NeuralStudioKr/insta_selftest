#!/bin/bash

# 로컬 개발 환경 시작 스크립트

echo "🚀 Instagram 댓글 관리 시스템 로컬 실행"
echo "========================================"

# 백엔드 실행
echo ""
echo "📦 백엔드 시작 중..."
cd backend

# 가상환경 확인 및 생성
if [ ! -d "venv" ]; then
    echo "가상환경 생성 중..."
    python3 -m venv venv
fi

# 가상환경 활성화
source venv/bin/activate

# 의존성 설치
if [ ! -f ".deps_installed" ]; then
    echo "의존성 설치 중..."
    pip install -r requirements.txt
    touch .deps_installed
fi

# .env 파일 확인
if [ ! -f ".env" ]; then
    echo "⚠️  .env 파일이 없습니다!"
    echo "backend/.env 파일을 생성하고 다음 변수들을 설정하세요:"
    echo "  - INSTAGRAM_ACCESS_TOKEN"
    echo "  - INSTAGRAM_APP_SECRET"
    echo "  - WEBHOOK_VERIFY_TOKEN"
    echo "  - API_BASE_URL=http://localhost:8000"
    exit 1
fi

echo "✅ 백엔드 서버 시작 (포트 8000)"
echo "   API 문서: http://localhost:8000/docs"
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

cd ..

# 프론트엔드 실행
echo ""
echo "📦 프론트엔드 시작 중..."
cd frontend

# 의존성 확인
if [ ! -d "node_modules" ]; then
    echo "의존성 설치 중..."
    npm install
fi

# .env.local 파일 확인
if [ ! -f ".env.local" ]; then
    echo "⚠️  .env.local 파일이 없습니다!"
    echo "frontend/.env.local 파일을 생성하고 다음을 설정하세요:"
    echo "  NEXT_PUBLIC_API_URL=http://localhost:8000"
    exit 1
fi

echo "✅ 프론트엔드 서버 시작 (포트 3000)"
echo "   웹사이트: http://localhost:3000"
npm run dev &
FRONTEND_PID=$!

cd ..

echo ""
echo "========================================"
echo "✅ 서버가 실행 중입니다!"
echo ""
echo "백엔드: http://localhost:8000"
echo "프론트엔드: http://localhost:3000"
echo "API 문서: http://localhost:8000/docs"
echo ""
echo "종료하려면 Ctrl+C를 누르세요."
echo "========================================"

# 종료 시그널 처리
trap "echo ''; echo '서버 종료 중...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM

# 프로세스 대기
wait
