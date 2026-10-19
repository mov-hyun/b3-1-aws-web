# 실제 검증 증빙

검증일: **2026-10-19**, 리전: **서울 ap-northeast-2**, 사용자: **b3-1-lab + 인증 앱 MFA**.

## 실제 AWS 구성

| 항목 | 실제 확인 결과 |
|---|---|
| VPC | vpc-03e10d298aa4cfe69, 10.31.0.0/16, Available |
| Public Subnet | subnet-079fb16d7994f562e, 10.31.1.0/24, ap-northeast-2a |
| Internet Gateway | igw-0d74537870ddac231, 위 VPC에 Attached |
| Route Table | rtb-096d76633cf668831, 0.0.0.0/0 → 위 IGW Active, 위 Subnet 명시적 연결 |
| Security Group | sg-00094eb9c5909f0c3, 인바운드 2개: TCP 80 전체 IPv4, TCP 22 실행 시점 학습자 공인 IP /32 |
| EC2 | i-0f0e25192b43a666e, t3.micro, Amazon Linux 2023, 19:34:04 KST 생성 |
| IP | 퍼블릭 3.36.67.14, 프라이빗 10.31.1.236. 자동 할당 공인 IP, Elastic IP 미사용 |
| EBS | vol-054f18e547a69947d, gp3 8 GiB, 암호화 예, 종료 시 삭제 예 |
| 운영 설정 | IMDSv2 Required, CPU 크레딧 standard, 상세 모니터링 비활성, 인스턴스 IAM Role 없음 |
| IAM | B31LabEC2Seoul, B31LabOwnMFA, IAMUserChangePassword만 연결. 관리자 정책 없음 |

비공개 콘솔 원본은 Git 제외 경로 .local/proof/에 보관했습니다. route-subnet-associated.png, security-group-created.png, ec2-launched.png 등에서 생성 당시 상태를 확인했습니다. 계정 화면·개인키·MFA 비밀정보는 공개 제출 파일에 포함하지 않습니다.

## SSH 및 서버 검증

19:37:24~26 KST 로컬 Windows OpenSSH로 접속했습니다. AWS 시스템 로그의 ED25519 지문과 ssh-keyscan 결과를 대조한 뒤 별도 known_hosts에 저장하고 StrictHostKeyChecking=yes로 연결했습니다.

| 검증 | 실제 결과 |
|---|---|
| hostname / id -un | ip-10-31-1-236.ap-northeast-2.compute.internal / ec2-user |
| systemctl is-active nginx | active |
| systemctl is-enabled nginx | enabled |
| nginx -t | syntax is ok, test is successful |
| curl -i http://localhost/health | HTTP/1.1 200 OK, 본문 OK |
| curl http://localhost | HTTP 200 |
| curl https://example.com | HTTPS 200 |

원본: [server-verification.txt](logs/server-verification.txt). 검증 당시 명령 기록: [verification-commands.md](logs/verification-commands.md).

nginx -t에 기본 MIME 해시 크기 경고가 있었으나 검사 종료 성공, 실제 응답은 정상이었습니다. 초기 user-data의 curl 패키지 충돌은 [트러블슈팅](troubleshooting.md)에 기록했습니다. 원래 실패한 cloud-init 실행을 성공으로 바꾸어 기록하지 않습니다.

## 외부 접속 검증 — 방식 B

명령: `curl.exe --noproxy '*' --fail --silent --show-error -i http://3.36.67.14/health`

2026-10-19 **19:37:35 KST**에 EC2 외부의 로컬 PC에서 실행했습니다. 결과는 **HTTP/1.1 200 OK**, 본문 **OK**입니다.

- [원본 HTTP 응답](logs/external-health.txt)
- [실제 실행 로그 스크린샷](screenshots/external-health.png)

스크린샷은 실제 저장 로그를 읽는 로컬 HTML 뷰어를 캡처했습니다. 이 뷰어 자체는 AWS로 요청하지 않습니다. 자동화 브라우저의 공인 IP 직접 열기는 ERR_BLOCKED_BY_CLIENT로 표시되어 방식 A의 성공 증빙으로 사용하지 않았습니다. 외부 HTTP 요청의 성공은 원본 curl 로그와 응답 시각으로 확인했습니다.

## 준비 단계 검증

- Python 단위 검사 4개 통과: here-document 삽입 경계, 16 KiB 제한, IAM 정책 범위.
- 최초 3,805 bytes user-data의 Bash 문법 검사 통과 후 실제 배포에서 패키지 충돌 발견.
- 수정 user-data 3,938 bytes를 같은 EC2에서 실행해 설치와 Nginx 검증 성공, 단위 검사 4개 재통과.
- 아키텍처 PNG를 실제 구성으로 갱신하고 이미지에서 구성 요소·화살표·문자 겹침 확인.
- 루트 MFA 및 액세스 키 0개 확인. 인증 앱 MFA 복구 후 과제용 IAM으로 조회·네트워크 및 EC2 생성 성공.

정책의 지역·MFA·태그 제한은 JSON에서 확인했습니다. 금지된 각 작업을 실제 호출한 부정 테스트까지 수행했다는 뜻은 아닙니다.

## 정리

실제 삭제 상태와 시각은 [cleanup-checklist.md](cleanup-checklist.md), [resources.json](resources.json)에 기록합니다. 검증 후 EC2 종료와 실습 네트워크·키 페어 삭제를 완료했습니다. EBS·Elastic IP·NAT·ENI 목록은 모두 0개였습니다. Billing 최종 금액은 권한 제한으로 재확인하지 않았습니다.
