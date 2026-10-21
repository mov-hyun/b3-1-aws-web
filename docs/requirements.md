# 요구사항과 증빙 매핑

아래 필수 실습은 2026-10-19의 검증·정리 기록입니다. 2026-10-21 보너스는 별도 자원에서 검증했고 정리도 완료했습니다.

| 요구사항 | 증빙 위치 | 현재 상태 |
|---|---|---|
| VPC 1개, Public Subnet 1개, IGW 연결 | architecture.png, resources.json, evidence.md | 생성·연결 확인 |
| 0.0.0.0/0 → IGW, 외부 아웃바운드 | evidence.md, logs/server-verification.txt | 경로 Active, HTTPS 200 |
| EC2 1대, SSH 접속 | resources.json, logs/server-verification.txt | 실제 SSH 성공 |
| Nginx 실행, localhost 200 | logs/server-verification.txt | active·enabled, localhost 200 |
| HTTP 80 공개, SSH 22 내 IP 제한 | evidence.md, 비공개 콘솔 원본 | 인바운드 2개 확인, 전체 포트 공개 없음 |
| 최소권한 IAM 사용자 또는 Role | infra/iam-policy.json, account-setup.md | b3-1-lab MFA 세션에서 생성 성공 |
| 관리자 권한 미부여 | account-setup.md, 비공개 정책 목록 | 연결 정책 3개, 관리자 정책 없음 |
| 외부 /health 200 및 OK | README, logs/external-health.txt, screenshots/external-health.png | 방식 B, 2026-10-19 19:37:35 KST 성공 |
| 트러블슈팅 최소 1건 | troubleshooting.md | 실제 로그인·설치 장애 2건 해결 |
| EC2/EBS/EIP/IGW/VPC 정리 | cleanup-checklist.md, resources.json | 종료·삭제 및 잔여 목록 확인 완료 |

제출 파일: docs/architecture.png, 외부 접속 결과 스크린샷, docs/troubleshooting.md, docs/cleanup-checklist.md. README에 실제 URL과 방식 B를 명시했습니다. 계정 전체 Billing 재확인은 권장 항목으로 남겼으며, 실습 자원 정리는 완료했습니다.

## 2026-10-21 선택 보너스

| 요구사항 | 증빙 위치 | 결과 |
|---|---|---|
| 무료 서브도메인·HTTPS 인증서 | bonus.md, logs/bonus-external-verification.txt, screenshots/bonus-https-page.png | Let's Encrypt 신뢰·호스트 이름 검사, HTTPS 200 |
| Docker 내부 localhost 정상 응답 | logs/bonus-server-verification.txt | localhost /와 /health 200 |
| Docker 외부 HTTP 접속 | logs/bonus-external-verification.txt | 방식 B, 공인 IP /health 200·OK |
| 이미지명·실행 방식·포트 매핑 | README, bonus.md, scripts/build_bonus_user_data.py | 실제 digest, docker run, TCP 80:80·443:443 기록 |
| Docker Up·외부 접속 스크린샷 2장 이상 | screenshots/bonus-docker-up.png, bonus-external-health.png, bonus-https-page.png | 로그 뷰어 2장·실제 HTTPS 페이지 1장 |
| 보너스 자원 정리 | bonus-resources.json, cleanup-checklist.md | 2026-10-21 13:06:29 KST 종료·삭제 확인 완료 |
