# 요구사항과 증빙 매핑

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
