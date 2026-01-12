# Instagram OAuth 문제 해결 가이드

## "앱 ID 오류: 입력된 앱 ID가 유효한 앱 ID와 다릅니다" 해결 방법

### 1단계: Meta App 대시보드에서 App ID 확인

1. [Meta for Developers](https://developers.facebook.com/apps/) 접속
2. 앱 선택
3. **설정 → 기본** 메뉴로 이동
4. **"앱 ID"** 확인
5. `.env` 파일의 `INSTAGRAM_APP_ID`와 비교

```bash
# .env 파일 확인
cd backend
cat .env | grep INSTAGRAM_APP_ID
```

**중요**: App ID가 일치하지 않으면 `.env` 파일을 수정하세요.

### 2단계: Facebook Login 제품 추가

1. Meta App 대시보드 → 왼쪽 메뉴
2. **"제품 추가"** 클릭
3. **"Facebook 로그인"** 선택
4. 설정 완료

### 3단계: OAuth 리디렉션 URI 설정

1. 왼쪽 메뉴 → **"Facebook 로그인"** → **"설정"**
2. **"유효한 OAuth 리디렉션 URI"** 섹션 찾기
3. 다음 URL을 **정확히** 추가 (대소문자, 슬래시까지 정확히):
   ```
   http://localhost:8000/api/auth/instagram/callback
   ```
4. **저장** 클릭

### 4단계: 플랫폼 추가 (웹사이트)

1. **설정 → 기본**
2. **"플랫폼 추가"** 클릭
3. **"웹사이트"** 선택
4. **사이트 URL** 입력: `http://localhost:8000`
5. **저장**

### 5단계: 앱 도메인 설정

1. **설정 → 기본**
2. **"앱 도메인"** 섹션
3. `localhost` 추가
4. **저장**

### 6단계: 앱 상태 확인

- **개발 모드**: 테스트 사용자만 로그인 가능
- **라이브 모드**: 모든 사용자 로그인 가능 (검토 필요)

개발 중에는 **개발 모드**로 사용 가능합니다.

### 7단계: 테스트 사용자 추가 (개발 모드인 경우)

1. **역할 → 역할** 메뉴
2. **"테스트 사용자"** 탭
3. **"테스트 사용자 추가"** 클릭
4. Facebook 계정으로 로그인하여 테스트

## 일반적인 오류와 해결 방법

### 오류: "리디렉션 URI 불일치"

**원인**: OAuth 리디렉션 URI가 정확히 일치하지 않음

**해결**:
- Meta App 대시보드에서 리디렉션 URI 확인
- `.env` 파일의 `OAUTH_REDIRECT_URI` 확인
- 대소문자, 슬래시까지 정확히 일치해야 함

### 오류: "권한이 없습니다"

**원인**: 필요한 권한이 승인되지 않음

**해결**:
- 앱 검토에서 다음 권한 승인:
  - `instagram_basic`
  - `instagram_manage_comments`
  - `pages_read_engagement`

### 오류: "Instagram Business Account를 찾을 수 없습니다"

**원인**: Facebook Page에 Instagram Business Account가 연결되지 않음

**해결**:
1. Facebook Page 생성
2. Instagram Business Account를 Facebook Page에 연결
3. Meta App에서 해당 Page에 연결

## 디버깅 팁

### OAuth URL 확인

```bash
curl http://localhost:8000/api/auth/instagram/url
```

응답에서 `app_id`와 `redirect_uri`를 확인하세요.

### 서버 로그 확인

```bash
# 백엔드 서버 로그 확인
tail -f /tmp/uvicorn.log
```

### 브라우저 개발자 도구

1. F12 키로 개발자 도구 열기
2. Network 탭 확인
3. OAuth 요청의 응답 확인

## 추가 도움말

- [Facebook Login 문서](https://developers.facebook.com/docs/facebook-login/)
- [Instagram Graph API 문서](https://developers.facebook.com/docs/instagram-api/)
- [Meta App 설정 가이드](https://developers.facebook.com/docs/apps/)
