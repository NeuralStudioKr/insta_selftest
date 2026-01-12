# Railway GitHub 앱 설치 문제 해결

## ❌ 하지 말아야 할 것

### "Revoke access" 버튼을 누르면?

**절대 하지 마세요!**

"Revoke access"를 누르면:
- ✅ 개인 계정에서 Railway App 접근이 **완전히 취소**됨
- ✅ 현재 설치된 앱이 **제거**됨
- ❌ 문제가 해결되지 않고 **오히려 더 악화**됨
- ❌ 다시 처음부터 설치해야 함

## ✅ 올바른 해결 방법

### 현재 상황
- ✅ 개인 계정 (`ns-cso`): Railway App 설치됨
- ❌ 조직 (`NeuralStudioKr`): Railway App 설치되지 않음

### 문제의 핵심
개인 계정에만 설치되어 있어서는 **조직 저장소에 접근할 수 없습니다**.

조직 저장소(`NeuralStudioKr/insta_selftest`)를 사용하려면 **조직 레벨에서 Railway App을 설치**해야 합니다.

### 해결 방법 1: GitHub 조직 설정에서 설치

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
   - `insta_selftest` 저장소 선택 (또는 모든 저장소)

### 해결 방법 2: Railway에서 설치 시도

1. **Railway 대시보드 접속**:
   ```
   https://railway.app
   ```

2. **Settings → GitHub**:
   - Railway 대시보드에서 Settings 클릭
   - "Connect GitHub" 또는 "GitHub" 섹션 클릭

3. **조직 선택 및 설치**:
   - "Install Railway App" 클릭
   - 조직(`NeuralStudioKr`) 선택
   - GitHub에서 권한 승인 페이지로 리디렉션
   - "Install" 또는 "Grant" 클릭

### 해결 방법 3: 조직 관리자에게 요청

조직 Owner 또는 Admin 권한이 없다면:

1. **조직 관리자 확인**:
   ```
   https://github.com/orgs/NeuralStudioKr/people
   ```
   - "Owners" 탭에서 관리자 확인

2. **요청 메시지**:
   ```
   안녕하세요,
   
   Railway를 통해 NeuralStudioKr/insta_selftest 저장소를 배포하려고 하는데,
   조직 레벨에서 Railway GitHub 앱 설치가 필요합니다.
   
   요청 사항:
   1. NeuralStudioKr 조직에 Railway GitHub 앱 설치
   2. 설치 페이지: https://github.com/organizations/NeuralStudioKr/settings/installations
   
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

## 요약

| 작업 | 결과 |
|------|------|
| ❌ "Revoke access" 클릭 | 앱 제거, 문제 악화 |
| ✅ 조직 레벨에서 설치 | 문제 해결 |

**핵심**: "Revoke access"가 아니라 **조직 레벨에서 Railway App을 설치**해야 합니다!
