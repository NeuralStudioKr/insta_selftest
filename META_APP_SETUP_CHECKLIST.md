# Meta App 대시보드 설정 체크리스트 (로컬 환경)

## 현재 코드 설정 확인

### 1. OAuth 리디렉션 URI
- **코드 설정**: `http://localhost:8000/api/auth/instagram/callback`
- **Meta App 설정 위치**: Facebook 로그인 → 설정 → 유효한 OAuth 리디렉션 URI
- **확인 필요**: 이 URL이 정확히 추가되어 있는지 확인

### 2. Webhook 콜백 URL
- **코드 엔드포인트**: `http://localhost:8000/webhook` (GET 및 POST)
- **Meta App 설정 위치**: Instagram 제품 → Webhooks 구성 → 콜백 URL
- **주의**: 로컬 환경에서는 ngrok 같은 터널링 서비스가 필요합니다
  - ngrok 사용 시: `https://your-ngrok-url.ngrok.io/webhook`
  - 또는 로컬 개발 중에는 Webhook을 사용하지 않고 Polling 방식 사용

### 3. Webhook 인증 토큰
- **코드 설정**: `.env` 파일의 `WEBHOOK_VERIFY_TOKEN`
- **Meta App 설정 위치**: Instagram 제품 → Webhooks 구성 → 인증 토큰
- **확인 필요**: 두 값이 일치해야 함

## Meta App 대시보드 설정 단계

### 단계 1: Facebook Login 설정 (OAuth용)

1. **Meta App 대시보드** → 왼쪽 메뉴 → **"Facebook 로그인"**
2. **"설정"** 탭 클릭
3. **"유효한 OAuth 리디렉션 URI"** 섹션에서 다음 URL 추가:
   ```
   http://localhost:8000/api/auth/instagram/callback
   ```
4. **저장** 클릭

### 단계 2: Instagram Webhook 설정 (선택사항 - 로컬 개발 시)

**참고**: 로컬 환경에서는 Webhook을 사용하려면 ngrok 같은 터널링 서비스가 필요합니다.

#### 옵션 A: ngrok 사용 (Webhook 테스트용)

1. ngrok 설치 및 실행:
   ```bash
   ngrok http 8000
   ```
2. ngrok에서 제공하는 HTTPS URL 복사 (예: `https://abc123.ngrok.io`)
3. Meta App 대시보드 → **Instagram 제품** → **Webhooks 구성**
4. **콜백 URL** 입력:
   ```
   https://abc123.ngrok.io/webhook
   ```
5. **인증 토큰** 입력: `.env` 파일의 `WEBHOOK_VERIFY_TOKEN` 값
6. **"확인 및 저장"** 클릭

#### 옵션 B: Polling 사용 (로컬 개발 권장)

로컬 개발 중에는 Webhook 대신 Polling 방식을 사용하는 것을 권장합니다:
- Webhook 설정 없이 사용 가능
- 프론트엔드의 "동기화" 버튼으로 댓글 가져오기
- 또는 백그라운드에서 주기적으로 Polling

### 단계 3: 플랫폼 추가

1. **설정** → **기본**
2. **"플랫폼 추가"** 클릭 → **"웹사이트"** 선택
3. **사이트 URL** 입력: `http://localhost:8000`
4. **저장**

### 단계 4: 앱 도메인 설정

1. **설정** → **기본**
2. **"앱 도메인"** 섹션
3. `localhost` 추가
4. **저장**

## 현재 설정 확인 명령어

```bash
# .env 파일 확인
cd backend
cat .env | grep -E "OAUTH_REDIRECT_URI|WEBHOOK_VERIFY_TOKEN|INSTAGRAM_APP_ID"

# OAuth URL 생성 테스트
curl http://localhost:8000/api/auth/instagram/url

# Webhook 엔드포인트 확인
curl http://localhost:8000/webhook?hub.mode=subscribe&hub.verify_token=YOUR_TOKEN&hub.challenge=test
```

## 중요 사항

### 로컬 환경의 제한사항

1. **Webhook은 공개 URL 필요**
   - 로컬 환경(`localhost`)은 외부에서 접근 불가
   - Webhook을 사용하려면 ngrok 같은 터널링 서비스 필수
   - 또는 Polling 방식 사용 (현재 구현됨)

2. **OAuth는 로컬에서 작동 가능**
   - `http://localhost:8000`은 OAuth 리디렉션에 사용 가능
   - Meta App에서 `localhost`를 허용해야 함

3. **앱 상태**
   - 개발 모드: 테스트 사용자만 로그인 가능
   - 라이브 모드: 모든 사용자 로그인 가능 (검토 필요)

## 설정 확인 체크리스트

- [ ] Facebook Login 제품이 추가되어 있음
- [ ] OAuth 리디렉션 URI가 정확히 설정됨: `http://localhost:8000/api/auth/instagram/callback`
- [ ] 플랫폼에 "웹사이트"가 추가되어 있음
- [ ] 앱 도메인에 `localhost`가 추가되어 있음
- [ ] (선택) Webhook 콜백 URL 설정 (ngrok 사용 시)
- [ ] (선택) Webhook 인증 토큰 설정 (ngrok 사용 시)

## 문제 해결

### "앱 ID 오류" 발생 시
1. Meta App 대시보드에서 실제 App ID 확인
2. `.env` 파일의 `INSTAGRAM_APP_ID`와 비교
3. 일치하지 않으면 `.env` 파일 수정

### OAuth 리디렉션 오류 발생 시
1. Meta App 대시보드에서 리디렉션 URI 확인
2. 대소문자, 슬래시까지 정확히 일치하는지 확인
3. `http://localhost:8000/api/auth/instagram/callback` (정확히 이 형식)

### Webhook이 작동하지 않을 때
1. 로컬 환경에서는 Webhook이 작동하지 않음 (정상)
2. Polling 방식 사용 (동기화 버튼)
3. Webhook 테스트를 원하면 ngrok 사용
