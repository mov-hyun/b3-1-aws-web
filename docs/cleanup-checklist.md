# 리소스 정리 체크리스트

현재 상태: **실습 자원 종료·삭제 완료**. 최종 확인 시각: **2026-10-19 19:49:51 KST** (`2026-10-19T10:49:51Z`).

사용자 삭제 승인 후 서울 리전에서 직접 확인했습니다. 식별자는 삭제 전 자원의 기록입니다.

| 항목 | 최종 상태 | 실제 확인 근거 |
|---|---|---|
| EC2 | 종료됨 / Terminated | i-0f0e25192b43a666e 종료 성공, 상태 전환 2026-10-19 10:45:35 UTC |
| EBS | 루트 볼륨 삭제, 서울 전체 볼륨 0개 | vol-054f18e547a69947d, 볼륨 목록의 “현재 이 리전에 볼륨이 없습니다”, 총 볼륨 수 0 |
| 자동 할당 공인 IP | 반환 완료 | 종료된 인스턴스의 공인 IP·자동 할당 IP가 비어 있음. 3.36.67.14는 과거 검증 주소 |
| Elastic IP | 미할당, 서울 목록 0개 | “이 리전에서 탄력적 IP 주소를 찾을 수 없음”. 할당한 적 없어 Release 작업 불필요 |
| Internet Gateway | Detach 및 삭제 완료 | VPC 삭제 성공 상세에 igw-0d74537870ddac231 포함 |
| Subnet | 삭제 완료 | 삭제 성공 상세에 subnet-079fb16d7994f562e 포함 |
| 별도 Route Table | 연결 해제 및 삭제 완료 | 삭제 성공 상세에 rtb-096d76633cf668831 포함 |
| Security Group | 삭제 완료 | 삭제 성공 상세에 sg-00094eb9c5909f0c3 포함 |
| VPC | 삭제 완료 | vpc-03e10d298aa4cfe69 삭제 성공. 전체 VPC 목록에는 기존 기본 VPC 1개만 남음 |
| EC2 키 페어 | AWS 등록 키 삭제 완료 | b3-1-web-key 삭제 성공, “표시할 키 페어 없음” |
| ENI | 서울 목록 0개 | “이 리전에는 네트워크 인터페이스가 없음” |
| NAT Gateway | 미생성, 서울 목록 0개 | “NAT 게이트웨이를 찾을 수 없음” |
| ELB / ALB | 실습에서 생성하지 않음 | 생성 작업 미수행, 실습 IAM에 ELB 생성 권한 없음. 계정 전체 목록 조회는 권한 없음 |
| RDS | 실습에서 생성하지 않음 | 생성 작업 미수행, 실습 IAM에 RDS 권한 없음. 계정 전체 목록 조회는 권한 없음 |

## 완료 체크

- [x] 접속 결과·장애 해결·설정 스크린샷과 로그 확보 후 삭제.
- [x] EC2 종료됨 확인.
- [x] EBS 실제 목록 0개 확인.
- [x] 자동 공인 IP 반환 및 Elastic IP 미할당 확인.
- [x] Subnet 라우팅 연결 해제, 별도 Route Table 삭제.
- [x] IGW 연결 해제 및 삭제.
- [x] 실습 Subnet·Security Group·VPC 삭제.
- [x] AWS의 실습 EC2 키 페어 삭제.
- [x] ENI·NAT 목록 잔여 없음 확인. ELB/ALB·RDS는 실습에서 미생성.
- [x] resources.json에 실제 식별자·최종 상태·시각 기록.
- [ ] 권장: 계정 소유자가 Billing Dashboard에서 반영된 사용 내역·잔여 크레딧 확인.

Billing은 과제용 IAM에 조회 권한이 없어 정리 후 청구 금액·잔여 크레딧을 재확인하지 않았습니다. 삭제 완료를 청구액 0달러의 근거로 사용하지 않습니다. 현재 무료 플랜을 유료 플랜으로 전환하지 않았습니다.

## 유지한 항목

기존 기본 VPC vpc-0cebb92cffb5d44e6와 공유 기본 DHCP 옵션은 보존했습니다. 루트·과제용 IAM 사용자와 MFA, 기존 B7-1 코드·Git 설정·Render 서비스·DB도 유지했습니다.

로컬 PEM 원본과 .local/의 작업용 복사본은 유지했습니다. AWS 키 페어와 서버는 삭제됐으며, 개인키 파일은 Git 제외 상태입니다. 이 체크리스트는 AWS 실습 자원 정리 결과입니다.

원본 콘솔 스크린샷은 Git 제외 경로 .local/proof/에 보관했습니다: ec2-terminated.png, ebs-empty.png, vpc-and-dependencies-deleted.png, key-pair-deleted.png, elastic-ip-empty.png, nat-empty.png, eni-empty.png.
