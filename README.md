# Instagram 댓글 관리 시스템

인스타그램 댓글을 자동으로 수집하고 웹페이지에서 관리할 수 있는 시스템입니다. 웹훅을 통해 실시간으로 댓글을 수신하고, 웹페이지에서 작성한 답글이 인스타그램에 자동으로 게시됩니다.

## 기술 스택

- **백엔드**: FastAPI (Python)
- **프론트엔드**: Next.js 14 (TypeScript, React)
- **데이터 저장**: JSON 파일 (프로토타입)
- **API**: Instagram Graph API

## 주요 기능

- ✅ 인스타그램 댓글 자동 수집 (웹훅)
- ✅ 댓글 목록 조회 및 검색
- ✅ 댓글에 답글 작성 (인스타그램에 자동 게시)
- ✅ 실시간 댓글 업데이트 (폴링)
- ✅ 댓글 삭제 기능

## 프로젝트 구조

```
insta/
├── backend/                 # FastAPI 백엔드
│   ├── main.py             # 메인 애플리케이션
│   ├── config.py           # 설정 관리
│   ├── routers/            # API 라우터
│   │   ├── webhook.py      # 웹훅 엔드포인트
│   │   └── comments.py     # 댓글 관리 API
│   ├── services/           # 비즈니스 로직
│   │   ├── storage.py      # JSON 저장소
│   │   └── instagram_client.py  # Instagram API 클라이언트
│   ├── data/               # 데이터 저장 디렉토리
│   │   └── comments.json   # 댓글 데이터
│   └── requirements.txt    # Python 의존성
│
├── frontend/               # Next.js 프론트엔드
│   ├── app/                # Next.js App Router
│   │   ├── page.tsx        # 메인 페이지
│   │   └── layout.tsx      # 레이아웃
│   ├── components/         # React 컴포넌트
│   │   └── CommentCard.tsx # 댓글 카드 컴포넌트
│   ├── lib/                # 유틸리티
│   │   └── api.ts          # API 클라이언트
│   └── package.json        # Node.js 의존성
│
└── README.md               # 프로젝트 문서
```

## 설치 및 실행

### 1. 백엔드 설정

```bash
# 백엔드 디렉토리로 이동
cd backend

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일을 편집하여 Instagram API 토큰 등을 설정
```

### 2. 프론트엔드 설정

```bash
# 프론트엔드 디렉토리로 이동
cd frontend

# 의존성 설치
npm install

# 환경 변수 설정
# .env.local 파일 생성
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

### 3. 실행

#### 방법 1: 자동 스크립트 사용 (권장)

**Linux/Mac:**
```bash
chmod +x scripts/start_local.sh
./scripts/start_local.sh
```

**Windows:**
```cmd
scripts\start_local.bat
```

#### 방법 2: 수동 실행

**백엔드 실행:**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**프론트엔드 실행:**
```bash
cd frontend
npm run dev
```

브라우저에서 `http://localhost:3000`으로 접속하세요.

### 4. 로컬에서 댓글 동기화 (폴링 방식)

웹훅 없이 로컬에서 댓글을 가져오려면 폴링 방식을 사용할 수 있습니다.

#### 방법 1: API 엔드포인트 사용

```bash
# 모든 미디어의 댓글 동기화 (최근 10개 미디어)
curl -X POST http://localhost:8000/api/comments/sync

# 특정 미디어의 댓글만 동기화
curl -X POST "http://localhost:8000/api/comments/sync?media_id=YOUR_MEDIA_ID"
```

#### 방법 2: 스크립트 사용

```bash
cd backend
python scripts/sync_comments.py --once --limit 10

# 주기적으로 동기화 (5분마다)
python scripts/sync_comments.py --interval 300 --limit 10
```

#### 방법 3: 프론트엔드에서 수동 동기화

프론트엔드의 "새로고침" 버튼을 클릭하면 저장된 댓글을 조회할 수 있습니다. 새로운 댓글을 가져오려면 위의 API나 스크립트를 사용하세요.

## Meta App 설정

### 1. Meta for Developers에서 앱 생성

1. [Meta for Developers](https://developers.facebook.com/)에 로그인
2. "내 앱" → "앱 만들기" 클릭
3. 앱 유형 선택 (예: "비즈니스" 또는 "기타")
4. 앱 이름 입력 후 생성

### 2. Instagram Graph API 추가

1. 앱 대시보드에서 "제품 추가" 클릭
2. "Instagram Graph API" 선택
3. 설정 완료

### 4. Instagram Business Account 연결

1. Instagram Graph API 설정 페이지로 이동
2. "Instagram Test User" 또는 "Instagram Business Account" 연결
3. 필요한 권한 요청:
   - `instagram_basic`
   - `instagram_manage_comments`
   - `pages_read_engagement`

### 5. Access Token 발급

1. "도구" → "Graph API 탐색기" 이동
2. 사용자 또는 페이지 선택
3. "액세스 토큰 생성" 클릭
4. 생성된 토큰을 `.env` 파일의 `INSTAGRAM_ACCESS_TOKEN`에 설정

### 6. 웹훅 설정 (선택사항 - 실시간 댓글 수신용)

> **참고**: 로컬에서 실행할 때는 웹훅 대신 폴링 방식을 사용할 수 있습니다. (위의 "로컬에서 댓글 동기화" 섹션 참고)

1. 앱 대시보드 → "제품" → "Instagram" → "웹훅" 이동
2. "새 구독 추가" 클릭
3. 콜백 URL 설정:
   - URL: `https://your-domain.com/webhook` (프로덕션)
   - 또는 로컬 테스트: `https://your-ngrok-url.ngrok.io/webhook`
4. 검증 토큰 설정: `.env` 파일의 `WEBHOOK_VERIFY_TOKEN` 값
5. 구독 필드: `comments` 선택
6. 저장

**로컬 개발 시 ngrok 사용:**
```bash
# ngrok 설치 (https://ngrok.com/)
# ngrok 실행
ngrok http 8000

# 생성된 URL 예시: https://abc123.ngrok.io
# Meta App 웹훅 설정에서 콜백 URL을 https://abc123.ngrok.io/webhook 으로 설정
```

**ngrok 주의사항:**
- 무료 플랜은 세션이 종료되면 URL이 변경됩니다
- ngrok을 재시작할 때마다 Meta App 웹훅 URL을 업데이트해야 합니다
- 로컬 개발 시에는 폴링 방식을 사용하는 것이 더 편리할 수 있습니다

### 7. App Secret 확인

1. 앱 설정 → "기본" 섹션
2. "앱 시크릿" 확인
3. `.env` 파일의 `INSTAGRAM_APP_SECRET`에 설정

## 환경 변수

### 백엔드 (.env)

```env
INSTAGRAM_ACCESS_TOKEN=your_access_token_here
INSTAGRAM_APP_SECRET=your_app_secret_here
WEBHOOK_VERIFY_TOKEN=your_webhook_verify_token_here
API_BASE_URL=http://localhost:8000
DATA_DIR=data
COMMENTS_FILE=comments.json
```

### 프론트엔드 (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## API 엔드포인트

### 웹훅

- `GET /webhook` - 웹훅 검증
- `POST /webhook` - 댓글 이벤트 수신

### 댓글 관리

- `GET /api/comments` - 댓글 목록 조회
  - Query Parameters:
    - `post_id` (optional): 특정 게시물의 댓글만 필터링
    - `limit` (default: 100): 최대 반환 개수
    - `offset` (default: 0): 건너뛸 개수
- `GET /api/comments/{comment_id}` - 특정 댓글 조회
- `POST /api/comments/{comment_id}/reply` - 댓글에 답글 작성
  - Body: `{ "message": "답글 내용" }`
- `DELETE /api/comments/{comment_id}` - 댓글 삭제
- `POST /api/comments/sync` - Instagram에서 댓글 동기화 (폴링)
  - Query Parameters:
    - `media_id` (optional): 특정 미디어의 댓글만 동기화
    - `limit` (default: 10): 동기화할 최근 미디어 개수 (media_id가 없을 때만 사용)

## 데이터 구조

### comments.json

```json
{
  "comments": [
    {
      "id": "instagram_comment_id",
      "post_id": "instagram_post_id",
      "text": "댓글 내용",
      "username": "사용자명",
      "timestamp": "2024-01-01T00:00:00Z",
      "replies": [
        {
          "id": "reply_id",
          "text": "답글 내용",
          "username": "me",
          "timestamp": "2024-01-01T01:00:00Z",
          "created_at": "2024-01-01T01:00:00Z"
        }
      ],
      "created_at": "2024-01-01T00:00:00Z",
      "like_count": 0
    }
  ]
}
```

## 주의사항

1. **Instagram Graph API 제한사항**:
   - Instagram Business Account 또는 Creator Account 필요
   - 일일 API 호출 제한이 있음
   - 웹훅은 프로덕션 환경에서만 정상 작동 (로컬 개발 시 ngrok 필요)

2. **보안**:
   - `.env` 파일은 절대 Git에 커밋하지 마세요
   - Access Token과 App Secret을 안전하게 관리하세요
   - 프로덕션 환경에서는 HTTPS를 사용하세요

3. **프로토타입**:
   - 현재는 JSON 파일로 데이터를 저장하는 프로토타입입니다
   - 프로덕션 환경에서는 데이터베이스(PostgreSQL, MongoDB 등) 사용을 권장합니다

## 문제 해결

### 웹훅이 작동하지 않는 경우

1. ngrok URL이 올바른지 확인
2. 웹훅 검증 토큰이 일치하는지 확인
3. Instagram Graph API 권한이 올바르게 설정되었는지 확인
4. 백엔드 서버가 실행 중인지 확인

### API 호출 실패

1. Access Token이 유효한지 확인
2. Instagram Business Account가 연결되었는지 확인
3. 필요한 권한이 부여되었는지 확인

## Railway 배포

### 1. Railway 계정 설정

1. [Railway](https://railway.app/)에 가입 및 로그인
2. GitHub 저장소와 연동 (Settings → Connect GitHub)

### 2. 백엔드 배포

1. Railway 대시보드에서 "New Project" 클릭
2. "Deploy from GitHub repo" 선택
3. 저장소 선택
4. **중요**: Settings → Root Directory를 `backend`로 설정
5. 환경 변수 설정 (Variables 탭):
   ```
   INSTAGRAM_ACCESS_TOKEN=your_instagram_access_token
   INSTAGRAM_APP_SECRET=your_app_secret
   WEBHOOK_VERIFY_TOKEN=your_webhook_verify_token
   API_BASE_URL=https://your-backend-url.railway.app
   FRONTEND_URL=https://your-frontend-url.railway.app
   ```
   > **참고**: `API_BASE_URL`과 `FRONTEND_URL`은 배포 후 생성된 URL로 업데이트해야 합니다.
6. 배포 시작 (자동으로 시작됨)
7. 배포 완료 후 생성된 URL 확인 (예: `https://your-backend.railway.app`)
8. Health check: `https://your-backend.railway.app/health` 접속하여 확인

### 3. 프론트엔드 배포

1. 같은 프로젝트에서 "New Service" 클릭
2. "Deploy from GitHub repo" 선택
3. 같은 저장소 선택
4. **중요**: Settings → Root Directory를 `frontend`로 설정
5. 환경 변수 설정 (Variables 탭):
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
   ```
   > **참고**: 백엔드 배포 후 생성된 URL을 사용하세요.
6. 배포 시작
7. 배포 완료 후 생성된 URL 확인

### 4. 웹훅 설정 업데이트

1. Meta App 대시보드로 이동
2. Instagram → 웹훅 설정 페이지 열기
3. 콜백 URL을 Railway 백엔드 URL로 업데이트:
   ```
   https://your-backend-url.railway.app/webhook
   ```
4. 검증 토큰은 Railway 환경 변수의 `WEBHOOK_VERIFY_TOKEN`과 동일하게 설정
5. 저장 후 웹훅 검증 테스트

### 5. CORS 설정 업데이트

백엔드 배포 후 프론트엔드 URL을 백엔드 환경 변수에 추가:
```
FRONTEND_URL=https://your-frontend-url.railway.app
```
또는 여러 URL 허용:
```
ALLOWED_ORIGINS=https://your-frontend-url.railway.app,https://another-domain.com
```

### 6. Railway 배포 주의사항

- **포트**: Railway는 `$PORT` 환경 변수를 자동으로 제공합니다. Procfile에서 이를 사용합니다.
- **데이터 영속성**: JSON 파일 저장소는 Railway의 임시 파일 시스템을 사용하므로, 재배포 시 데이터가 사라질 수 있습니다. 프로덕션 환경에서는 Railway PostgreSQL 또는 MongoDB 같은 데이터베이스 사용을 권장합니다.
- **환경 변수**: 민감한 정보는 Railway의 Variables 탭에서 관리하세요. Git에 커밋하지 마세요.
- **자동 배포**: GitHub에 푸시하면 자동으로 재배포됩니다. 필요시 Settings에서 비활성화할 수 있습니다.
- **빌드 시간**: 첫 배포는 시간이 걸릴 수 있습니다. 빌드 로그를 확인하세요.

### 7. Railway CLI 사용 (선택사항)

```bash
# Railway CLI 설치
npm i -g @railway/cli

# 로그인
railway login

# 프로젝트 연결
railway link

# 환경 변수 설정
railway variables set INSTAGRAM_ACCESS_TOKEN=your_token
railway variables set INSTAGRAM_APP_SECRET=your_secret
railway variables set WEBHOOK_VERIFY_TOKEN=your_token

# 로그 확인
railway logs

# 배포 상태 확인
railway status
```

### 8. 배포 체크리스트

- [ ] Railway 프로젝트 생성
- [ ] 백엔드 서비스 배포 (Root Directory: `backend`)
- [ ] 백엔드 환경 변수 설정
- [ ] 백엔드 Health check 통과
- [ ] 프론트엔드 서비스 배포 (Root Directory: `frontend`)
- [ ] 프론트엔드 환경 변수 설정 (`NEXT_PUBLIC_API_URL`)
- [ ] 백엔드 CORS 설정 업데이트 (`FRONTEND_URL`)
- [ ] Meta App 웹훅 URL 업데이트
- [ ] 웹훅 검증 테스트
- [ ] 프론트엔드에서 API 호출 테스트

## 라이선스

이 프로젝트는 프로토타입 목적으로 제작되었습니다.
