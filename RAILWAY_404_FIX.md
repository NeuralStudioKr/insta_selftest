# Railway GitHub 앱 설치 - 404 오류 해결

## 문제
GitHub 조직 설정 페이지(`/settings/installations`)에 접근 시 404 오류 발생

## 원인
1. **권한 부족**: Owner 또는 Admin 권한이 없음
2. **URL 경로 차이**: GitHub 인터페이스 변경으로 경로가 다를 수 있음
3. **접근 제한**: 조직 설정에 대한 접근 권한이 없음

## 해결 방법

### 방법 1: Railway에서 직접 설치 (가장 권장)

이 방법이 가장 쉽고 확실합니다:

1. **Railway 대시보드 접속**:
   ```
   https://railway.app
   ```

2. **Settings → GitHub**:
   - Railway 대시보드에서 "Settings" 클릭
   - "GitHub" 또는 "Connect GitHub" 섹션 클릭

3. **앱 설치**:
   - "Install Railway App" 또는 "Connect GitHub" 버튼 클릭
   - GitHub 인증 페이지로 리디렉션됨

4. **조직 선택 및 승인**:
   - GitHub 인증 페이지에서
   - "NeuralStudioKr" 조직 선택
   - "Install" 또는 "Grant" 클릭
   - 저장소 접근 권한 설정 (`insta_selftest` 선택)

### 방법 2: GitHub 조직 페이지에서 Settings 찾기

1. **조직 메인 페이지**:
   ```
   https://github.com/organizations/NeuralStudioKr
   ```

2. **Settings 탭 찾기**:
   - 상단 탭 메뉴에서 "Settings" 찾기
   - **주의**: Owner/Admin 권한이 있어야 보입니다

3. **Third-party access 찾기**:
   - Settings 페이지에서
   - 왼쪽 사이드바에서 "Third-party access" 또는 "Installed GitHub Apps" 클릭

### 방법 3: 조직 설정 메인 페이지

1. **조직 설정 메인**:
   ```
   https://github.com/organizations/NeuralStudioKr/settings
   ```

2. **왼쪽 사이드바에서 찾기**:
   - "Third-party access"
   - "Installed GitHub Apps"
   - "OAuth Apps"

### 방법 4: 권한이 없는 경우

만약 위 방법들이 모두 작동하지 않는다면:

1. **권한 확인**:
   ```
   https://github.com/orgs/NeuralStudioKr/people
   ```
   - 자신의 역할이 "Owner" 또는 "Admin"인지 확인

2. **조직 관리자에게 요청**:
   - "People" 탭에서 Owner 찾기
   - Owner에게 다음 메시지 전달:

   ```
   안녕하세요,
   
   Railway를 통해 NeuralStudioKr/insta_selftest 저장소를 배포하려고 하는데,
   조직 레벨에서 Railway GitHub 앱 설치가 필요합니다.
   
   요청 사항:
   1. Railway에서 GitHub 연결 시도
   2. 또는 GitHub 조직 설정에서 Railway 앱 설치
   
   설치 방법:
   - Railway: https://railway.app → Settings → GitHub → Install Railway App
   - GitHub: 조직 설정 → Third-party access → Railway App 설치
   
   감사합니다.
   ```

## 권장 순서

1. ✅ **Railway에서 직접 설치 시도** (가장 쉬움)
2. ✅ GitHub 조직 페이지에서 Settings 탭 찾기
3. ✅ 조직 설정 메인 페이지 접근
4. ✅ 조직 관리자에게 요청 (권한이 없는 경우)

## 확인 방법

설치가 완료되면:

1. **Railway에서**:
   - Settings → GitHub
   - NeuralStudioKr 조직이 목록에 나타남
   - 저장소 연결 시도 시 `insta_selftest` 저장소가 보임

2. **GitHub에서**:
   - 조직 설정 → Third-party access
   - Railway App이 목록에 나타남

## 추가 도움말

- [GitHub 조직 설정 문서](https://docs.github.com/en/organizations/managing-organization-settings)
- [Railway GitHub 연동](https://docs.railway.app/develop/github)
