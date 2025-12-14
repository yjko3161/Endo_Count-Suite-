# Endo Count Suite

Flask 기반 내시경 집계 대시보드 예제 애플리케이션입니다. 세션 기반 로그인과 관리자 기능을 포함하며, 공통 코드/의사/카테고리 관리를 통해 대시보드 구성을 데이터 기반으로 변경할 수 있습니다.

## 주요 기능
- 세션 기반 로그인 및 1아이디 1로그인 강제 (중복 로그인 시 이전 세션 만료)
- Admin/User 권한 분리, 메뉴 접근 제어
- 사용자 관리: 추가/수정/비활성화, 비밀번호 초기화, 강제 로그아웃
- 공통 코드/코드그룹 관리, 의사 관리, 카테고리 관리
- 기간 필터가 포함된 집계 대시보드 뷰와 합계 카드
- bcrypt 비밀번호 해시, CSRF 보호, SQLAlchemy ORM 사용

## 실행 방법
1. 의존성 설치
   ```bash
   pip install -r requirements.txt
   ```
2. 환경 변수로 데이터베이스 연결 문자열을 설정합니다. (기본값: SQLite `endo_count.db`)
   ```bash
   export DATABASE_URI="mysql+pymysql://user:password@localhost:3306/endo"
   export SECRET_KEY="change-me"
   ```
3. 애플리케이션 실행
   ```bash
   python run.py
   ```
4. 최초 관리자 계정은 `admin / admin1234`입니다.

## 데이터 모델
- `users`, `user_sessions`, `code_groups`, `codes`, `doctors`, `categories`, `procedure_logs`

## 반응형 UI
Bootstrap 5와 커스텀 CSS를 사용하여 모바일/태블릿/데스크탑 환경에서 가로 스크롤 테이블과 카드형 합계 영역이 자연스럽게 표시되도록 구성했습니다.
