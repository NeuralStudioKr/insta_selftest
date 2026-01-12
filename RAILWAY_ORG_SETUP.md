# Railway GitHub 앱 조직 설치 가이드

## 현재 상태

- ✅ 개인 계정 (`ns-cso`): Railway App 설치됨
- ❌ 조직 (`NeuralStudioKr`): Railway App 설치되지 않음

## 문제

Railway에서 조직 저장소(`NeuralStudioKr/insta_selftest`)를 연결하려면, 조직 레벨에서 Railway GitHub 앱을 설치해야 합니다.

개인 계정에만 설치되어 있어서는 조직 저장소에 접근할 수 없습니다.

## 해결 방법

### 방법 1: 조직 설정 페이지에서 직접 설치

1. **조직 설정 페이지로 이동**:
   ```
   https://github.com/organizations/NeuralStudioKr/settings/installations
   ```

2. **Railway App 찾기**:
   - 페이지에서 "Railway App" 검색
   - 또는 "Third-party access" 섹션에서 찾기

3. **설치/승인**:
   - "Configure" 또는 "Grant access" 클릭
   - 조직 저장소 접근 권한 승인
   - 필요한 저장소 선택 (또는 모든 저장소)

### 방법 2: 조직 Settings에서 설치

1. **조직 페이지로 이동**:
   ```
   https://github.com/organizations/NeuralStudioKr
   ```

2. **Settings 클릭**:
   - 조직 페이지에서 "Settings" 탭 클릭

3. **Third-party access 찾기**:
   - 왼쪽 사이드바에서 "Third-party access" 또는 "Installed GitHub Apps" 클릭

4. **Railway App 설치**:
   - "Install GitHub App" 또는 "Configure" 버튼 클릭
   - Railway App 선택
   - 저장소 접근 권한 설정

### 방법 3: Railway에서 설치 시도 (권장)

1. **Railway 대시보드 접속**:
   ```
   https://railway.app
   ```

2. **Settings → GitHub 연결**:
   - Railway 대시보드에서 Settings 클릭
   - "Connect GitHub" 또는 "GitHub" 섹션 클릭

3. **조직 선택 및 설치**:
   - "Install Railway App" 클릭
   - 조직(`NeuralStudioKr`) 선택
   - GitHub에서 권한 승인 페이지로 리디렉션
   - "Install" 또는 "Grant" 클릭

## 조직 관리자 권한 필요

**중요**: 조직 레벨에서 앱을 설치하려면 **조직 Owner 또는 Admin 권한**이 필요합니다.

### 권한 확인 방법

1. 조직 페이지 접속:
   ```
   https://github.com/orgs/NeuralStudioKr/people
   ```

2. 자신의 역할 확인:
   - "Owners" 또는 "Members" 탭에서 확인
   - "Owner" 또는 "Admin" 권한이 있어야 함

### 권한이 없는 경우

조직 Owner 또는 Admin에게 다음을 요청:

```
안녕하세요,

Railway를 통해 NeuralStudioKr/insta_selftest 저장소를 배포하려고 하는데,
조직 레벨에서 Railway GitHub 앱 설치가 필요합니다.

요청 사항:
1. NeuralStudioKr 조직에 Railway GitHub 앱 설치
2. 설치 페이지: https://github.com/organizations/NeuralStudioKr/settings/installations
3. 또는 Railway에서: https://railway.app → Settings → GitHub → Install Railway App

설치 후 자동 배포가 가능해집니다.

감사합니다.
```

## 설치 확인

설치가 완료되면:

1. **GitHub에서 확인**:
   ```
   https://github.com/organizations/NeuralStudioKr/settings/installations
   ```
   - Railway App이 목록에 나타나야 함

2. **Railway에서 확인**:
   - Railway → Settings → GitHub
   - NeuralStudioKr 조직이 목록에 나타남
   - 저장소 연결 시도 시 `insta_selftest` 저장소가 보임

## 다음 단계

설치 완료 후:

1. Railway에서 "New Project" 클릭
2. "Deploy from GitHub repo" 선택
3. NeuralStudioKr 조직 선택
4. `insta_selftest` 저장소 선택
5. 배포 시작

## 참고 링크

- [GitHub 조직 앱 설치 가이드](https://docs.github.com/en/organizations/managing-organization-settings/managing-third-party-access-for-your-organization)
- [Railway GitHub 연동](https://docs.railway.app/develop/github)
