# Meta App 대시보드 설정 가이드 (실제 화면 기준)

## 현재 위치
스크린샷 기준: **"이용 사례 맞춤 설정"** → **"Instagram API"** 페이지

## 설정 1: OAuth 리디렉션 URI 추가

### 경로 (스크린샷 기준):
1. **왼쪽 사이드바**에서 **"권한 및 기능"** (Permissions and Features) 섹션 찾기
2. **"Facebook 로그인이 포함된 API 설정"** (API Settings including Facebook Login) 클릭
   - 현재 "Instagram 로그인이 포함된 API 설정" 아래에 있을 것입니다
3. 해당 페이지에서 **"Facebook 로그인"** 또는 **"OAuth 설정"** 섹션 찾기
4. **"유효한 OAuth 리디렉션 URI"** (Valid OAuth Redirect URIs) 섹션 찾기
5. 다음 URL을 **정확히** 입력:
   ```
   http://localhost:8000/api/auth/instagram/callback
   ```
6. **"저장"** 또는 **"변경 사항 저장"** 클릭

### 대안 경로:
- 왼쪽 사이드바 맨 아래 또는 상단 메뉴에서 **"설정"** (Settings) 찾기
- **"제품"** (Products) 또는 **"Facebook 로그인"** 메뉴 찾기
- 또는 상단 검색창에서 "Facebook Login" 검색

---

## 설정 2: 플랫폼 추가 (웹사이트)

### 경로:
1. **왼쪽 사이드바** 맨 아래 또는 상단에서 **"설정"** (Settings) 아이콘/메뉴 찾기
   - ⚙️ 아이콘이 있을 수 있음
2. **"기본"** (Basic) 탭 클릭
3. 페이지 아래로 스크롤하여 **"플랫폼"** (Platforms) 섹션 찾기
4. **"플랫폼 추가"** (Add Platform) 버튼 클릭
5. **"웹사이트"** (Website) 선택
6. **"사이트 URL"** 입력란에 다음 입력:
   ```
   http://localhost:8000
   ```
7. **"저장"** 클릭

---

## 설정 3: 앱 도메인 추가

### 경로:
1. **왼쪽 사이드바**에서 **"설정"** (Settings) 클릭
2. **"기본"** (Basic) 탭 클릭
3. **"앱 도메인"** (App Domains) 섹션 찾기
4. 입력란에 다음 입력:
   ```
   localhost
   ```
5. **"저장"** 클릭

---

## 빠른 찾기 방법

### 방법 1: 왼쪽 사이드바에서 "Facebook 로그인" 찾기
1. 왼쪽 사이드바의 **"권한 및 기능"** 섹션 확인
2. **"Facebook 로그인이 포함된 API 설정"** 클릭
3. OAuth 설정 페이지에서 리디렉션 URI 추가

### 방법 2: 상단 메뉴에서 찾기
1. 페이지 상단의 메뉴바 확인
2. **"설정"** (Settings) 또는 ⚙️ 아이콘 클릭
3. **"제품"** (Products) 또는 **"Facebook 로그인"** 찾기

### 방법 3: 검색 기능 사용
1. 페이지 상단의 검색창 사용
2. "Facebook Login" 또는 "OAuth" 검색
3. 관련 설정 페이지로 이동

---

## 스크린샷에서 보이는 구조

```
왼쪽 사이드바:
├── 이용 사례
│   └── 맞춤 설정 (현재 위치)
├── 권한 및 기능
│   ├── Instagram 로그인이 포함된 API 설정 (현재 선택됨)
│   ├── API 통합 도우미
│   └── Facebook 로그인이 포함된 API 설정 ← 여기 클릭!
└── (아래쪽에 설정 메뉴가 있을 수 있음)
```

---

## 중요: 설정 메뉴 찾기

설정 메뉴는 다음 위치 중 하나에 있을 수 있습니다:
1. **왼쪽 사이드바 맨 아래**
2. **페이지 상단 메뉴바** (⚙️ 아이콘)
3. **드롭다운 메뉴** (프로필 아이콘 옆)

---

## 문제 해결

### "Facebook 로그인이 포함된 API 설정"을 찾을 수 없을 때
1. 왼쪽 사이드바를 위아래로 스크롤
2. "권한 및 기능" 섹션을 확장/축소
3. 페이지 상단의 검색창 사용

### 설정 메뉴를 찾을 수 없을 때
1. 브라우저 주소창에 직접 입력:
   ```
   https://developers.facebook.com/apps/YOUR_APP_ID/settings/basic/
   ```
   (YOUR_APP_ID를 실제 앱 ID로 변경)
2. 또는:
   ```
   https://developers.facebook.com/apps/YOUR_APP_ID/fb-login/settings/
   ```
