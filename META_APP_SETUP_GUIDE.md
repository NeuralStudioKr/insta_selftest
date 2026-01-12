# Meta App 대시보드 설정 가이드 (단계별)

## 현재 위치
스크린샷에서 보이는 페이지: **Instagram API 설정 페이지**

## 설정 1: OAuth 리디렉션 URI 추가

### 경로:
1. **왼쪽 사이드바**에서 **"제품"** 또는 **"Products"** 메뉴 클릭
2. **"Facebook 로그인"** (Facebook Login) 찾기
   - 없으면: **"제품 추가"** (Add Product) → **"Facebook 로그인"** 선택
3. **"Facebook 로그인"** 클릭
4. 왼쪽 메뉴에서 **"설정"** (Settings) 탭 클릭
5. **"유효한 OAuth 리디렉션 URI"** (Valid OAuth Redirect URIs) 섹션 찾기
6. 다음 URL을 **정확히** 입력:
   ```
   http://localhost:8000/api/auth/instagram/callback
   ```
7. **"변경 사항 저장"** (Save Changes) 클릭

### 스크린샷 위치:
- 왼쪽 사이드바 → 제품 → Facebook 로그인 → 설정

---

## 설정 2: 플랫폼 추가 (웹사이트)

### 경로:
1. **왼쪽 사이드바**에서 **"설정"** (Settings) 클릭
2. **"기본"** (Basic) 탭 클릭 (기본적으로 선택되어 있을 수 있음)
3. 페이지 아래쪽으로 스크롤하여 **"플랫폼"** (Platforms) 섹션 찾기
4. **"플랫폼 추가"** (Add Platform) 버튼 클릭
5. **"웹사이트"** (Website) 선택
6. **"사이트 URL"** (Site URL) 입력란에 다음 입력:
   ```
   http://localhost:8000
   ```
7. **"저장"** (Save) 클릭

### 스크린샷 위치:
- 왼쪽 사이드바 → 설정 → 기본 → 플랫폼 섹션

---

## 설정 3: 앱 도메인 추가

### 경로:
1. **왼쪽 사이드바**에서 **"설정"** (Settings) 클릭
2. **"기본"** (Basic) 탭 클릭
3. **"앱 도메인"** (App Domains) 섹션 찾기
   - "플랫폼" 섹션 근처에 있을 수 있음
4. **"앱 도메인 추가"** 또는 입력란에 다음 입력:
   ```
   localhost
   ```
5. **"저장"** (Save) 클릭

### 스크린샷 위치:
- 왼쪽 사이드바 → 설정 → 기본 → 앱 도메인 섹션

---

## 시각적 가이드

### 왼쪽 사이드바 구조:
```
📱 앱 대시보드
├── 📊 분석
├── 📝 제품 (Products)
│   ├── Facebook 로그인 ← 여기서 OAuth 설정
│   ├── Instagram
│   └── ...
├── ⚙️ 설정 (Settings) ← 여기서 플랫폼/도메인 설정
│   ├── 기본 (Basic)
│   ├── 고급
│   └── ...
└── ...
```

---

## 빠른 체크리스트

### 1단계: Facebook Login 제품 확인
- [ ] 왼쪽 사이드바 → 제품 → Facebook 로그인 존재 확인
- [ ] 없으면: 제품 추가 → Facebook 로그인 추가

### 2단계: OAuth 리디렉션 URI 설정
- [ ] Facebook 로그인 → 설정 탭
- [ ] "유효한 OAuth 리디렉션 URI"에 추가:
  ```
  http://localhost:8000/api/auth/instagram/callback
  ```
- [ ] 저장

### 3단계: 플랫폼 추가
- [ ] 설정 → 기본
- [ ] 플랫폼 섹션 → 플랫폼 추가 → 웹사이트
- [ ] 사이트 URL: `http://localhost:8000`
- [ ] 저장

### 4단계: 앱 도메인 추가
- [ ] 설정 → 기본
- [ ] 앱 도메인 섹션
- [ ] `localhost` 추가
- [ ] 저장

---

## 문제 해결

### "Facebook 로그인" 제품이 보이지 않을 때
1. 왼쪽 사이드바 → **"제품 추가"** (Add Product) 클릭
2. **"Facebook 로그인"** 찾기
3. **"설정"** 클릭하여 추가

### "설정" 메뉴를 찾을 수 없을 때
- 왼쪽 사이드바 맨 아래쪽에 있을 수 있음
- 또는 상단 메뉴바의 ⚙️ 아이콘 클릭

### 설정 후에도 오류가 발생할 때
1. 브라우저 캐시 삭제 (Ctrl+Shift+Delete)
2. Meta App 대시보드에서 설정이 저장되었는지 다시 확인
3. 서버 재시작:
   ```bash
   # 백엔드 서버 재시작
   pkill -f "uvicorn main:app"
   cd backend && source venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
   ```
