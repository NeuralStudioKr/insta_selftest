# Instagram OAuth 설정 가이드

## Meta App OAuth 설정

Instagram OAuth가 작동하려면 Meta App에서 다음 설정이 필요합니다:

### 1. Facebook Login 제품 추가

1. [Meta for Developers](https://developers.facebook.com/) → 앱 선택
2. "제품 추가" 클릭
3. "Facebook 로그인" 선택
4. 설정 완료

### 2. OAuth 리디렉션 URI 설정

1. 앱 대시보드 → Facebook 로그인 → 설정
2. "유효한 OAuth 리디렉션 URI"에 추가:
   ```
   http://localhost:8000/api/auth/instagram/callback
   ```
3. 프로덕션 환경의 경우:
   ```
   https://your-domain.com/api/auth/instagram/callback
   ```

### 3. 플랫폼 추가 (웹사이트)

1. 설정 → 기본
2. "플랫폼 추가" 클릭 → "웹사이트" 선택
3. 사이트 URL 입력:
   - 로컬: `http://localhost:8000`
   - 프로덕션: `https://your-domain.com`

### 4. 앱 도메인 설정

1. 설정 → 기본
2. "앱 도메인"에 추가:
   - 로컬: `localhost`
   - 프로덕션: `your-domain.com`

### 5. 필요한 권한 확인

앱 검토에서 다음 권한이 승인되어야 합니다:
- `instagram_basic`
- `instagram_manage_comments`
- `pages_read_engagement`

### 6. 테스트 모드 확인

개발 중에는:
- 앱이 "개발 모드"에 있어도 테스트 사용자로 로그인 가능
- 또는 앱을 "라이브 모드"로 전환 (검토 필요)

## 문제 해결

### "앱 ID 오류" 발생 시

1. Meta App 대시보드에서 App ID 확인
2. `.env` 파일의 `INSTAGRAM_APP_ID`가 정확한지 확인
3. OAuth 리디렉션 URI가 정확히 설정되었는지 확인
4. 앱이 활성화 상태인지 확인

### OAuth 리디렉션 URI 불일치 오류

- 리디렉션 URI가 정확히 일치해야 합니다 (대소문자, 슬래시 포함)
- `http://localhost:8000/api/auth/instagram/callback` (정확히 이 형식)
