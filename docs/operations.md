# 보안·장애 점검·확장·비용 대응

실제 수행 기록과 재운영 시 적용할 계획을 구분합니다. 두 차례 실습 자원은 모두 삭제했습니다. 아래 임계값·ALB·비용 알림·권한 변경 절차는 향후 운영 계획이며, 이번 실습에서 부하 시험이나 해당 서비스 생성을 수행했다는 뜻은 아닙니다.

## 1. 공개 접근의 목적·위험·기간

HTTP TCP 80의 소스 `0.0.0.0/0`는 모든 IPv4 주소에서 웹 포트로 접속할 수 있다는 뜻입니다. 과제의 불특정 외부 사용자 접속과 공인 IP /health 검증을 위해 허용했습니다. SSH TCP 22는 실행 시점 학습자의 공인 IP /32만 허용했습니다. 전체 포트 0–65535 공개 규칙은 생성하지 않았습니다.

공개 웹 포트에는 자동 스캔·취약점 공격·과도한 요청이 도달할 수 있습니다. HTTP 평문 통신에는 도청·변조 위험도 있습니다. 실습 페이지는 정적 콘텐츠와 /health만 제공했고 비밀번호·개인정보·비밀키를 웹에 배포하지 않았습니다. 보너스에서 HTTPS를 검증했으며, SSH 제한·포트 최소화·짧은 실행 기간·실습 후 삭제를 함께 적용했습니다. HTTPS를 적용한 뒤에도 웹 취약점과 과도한 요청에 대한 대응은 필요합니다.

| 실습 | 생성부터 종료 요청까지의 기록 | 외부 검증 | 최종 정리 확인 |
|---|---|---|---|
| 필수 | 2026-10-19 19:34:04~19:45:35 KST | 19:37:35 KST HTTP 200·OK | 19:49:51 KST |
| 보너스 | 2026-10-21 12:43:46~13:01:49 KST | 12:53:40 KST HTTP·HTTPS 200·OK | 13:06:29 KST |

이는 자원 수명 기록입니다. 전체 구간에 서비스가 응답했다고 측정한 것은 아닙니다. 증빙 확보 후 공개 규칙이 연결된 실습 자원도 함께 삭제했습니다.

| 운영 목적별 대안 | 적용 판단 |
|---|---|
| 특정 사용자만 쓰는 페이지 | 웹 포트도 허용 IP로 제한. 이 과제의 HTTP 전체 공개 검증을 마친 뒤 적용 |
| 관리자 접속 | SSH /32 유지. 반복 운영 시 VPN 또는 Systems Manager 기반 접속 검토. 필요한 권한·구성·비용을 먼저 확인 |
| 다중 서버 공개 서비스 | ALB에서 요청을 받고, EC2 웹 포트의 소스는 ALB의 SG로 제한하는 구성 검토 |

ALB·VPN은 이번에 생성하지 않았습니다. ALB는 공개 입구와 대상 서버를 분리할 수 있지만 웹 애플리케이션의 취약점과 권한 문제도 별도로 관리해야 합니다. 포트·소스 최소화와 SG의 상태 유지 특성은 [AWS SG 문서](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html)에 근거합니다.

## 2. SG·IAM·라우팅의 역할

| 구분 | 통제하는 것 | 이 실습의 예 |
|---|---|---|
| Security Group | 프로토콜·포트·출발지/목적지에 따른 네트워크 통신 | HTTP 80 공개, SSH 22 내 IP /32 |
| IAM | 누가 어떤 AWS API 작업을 어느 자원·조건에서 할 수 있는지 | b3-1-lab, 서울·MFA·Project 태그·micro·암호화 조건 |
| Route Table | 목적지 주소로 트래픽을 전달할 다음 경로 | 0.0.0.0/0 → IGW |

정적 웹페이지를 여는 방문자의 HTTP 요청은 SG와 웹 서버 설정에 따라 처리됩니다. EC2를 생성·종료하는 관리 요청은 IAM 정책으로 통제합니다. IAM 허용만으로 SSH 포트가 열리지 않으며, SG 허용만으로 AWS 관리 권한을 얻지 않습니다. [IAM 정책의 역할](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html).

경로표의 `0.0.0.0/0`는 모든 IPv4 **목적지**에 대한 기본 경로이고, SG 인바운드 소스의 `0.0.0.0/0`는 모든 IPv4 **출발지**를 뜻합니다. 두 설정의 용도를 구분합니다.

서버가 시작하는 아웃바운드 연결은 패키지 설치, Docker 이미지 다운로드, 인증서 발급·갱신, 외부 HTTPS 검증에 필요합니다. 실습에서는 기본 아웃바운드 허용을 사용했습니다. 재운영 시 실제 목적지·포트를 조사해 줄이되, 변하는 저장소·인증서 서버 주소도 고려합니다. SG는 상태를 유지하므로 허용된 인바운드 요청의 응답은 아웃바운드 규칙과 무관하게 허용됩니다. HTTP 응답을 위해 모든 인바운드 포트를 추가로 열 필요가 없습니다. [AWS의 응답 트래픽 설명](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html#security-group-basics).

## 3. 재실습 시 장애 점검 순서

새로 생성한 본인 자원에만 적용하는 절차입니다. 삭제·반환한 과거 IP에는 실행하지 않습니다.

| 순서 | 확인 수단 | 정상 판정과 조치 |
|---|---|---|
| 1. 라우팅 | Subnet 연결 경로표, IGW 연결, 기본 경로 확인 | 의도한 Subnet에 연결, 0.0.0.0/0 → 해당 IGW Active |
| 2. SG | 인스턴스에 실제 연결된 SG의 포트·소스 확인 | HTTP 80 공개, SSH 22 현재 내 IP /32. 광범위한 포트 허용 대신 필요한 규칙만 수정 |
| 3. 공인 IP | EC2 상태와 현재 공인 IPv4 확인 | Running과 현재 주소 확인. 중지·재시작 후 과거 주소를 그대로 사용하지 않음 |
| 4. 서버 | SSH 후 `systemctl is-active nginx` 또는 `sudo docker ps`, `curl -i http://localhost/health` | 서비스 active/Up 및 200·OK. 실패하면 bootstrap·cloud-init·서버 로그 조회 |
| 5. 외부 재검증 | 외부 PC에서 새 IP의 GET /health | 200·OK. 서버 접근 로그의 시각·상태와 대조 |
| 관리 API 거부 | 사용자·MFA·리전·태그·API 이름·정책 조건 확인 | AccessDenied는 IAM 경로에서 조사. 네트워크 접속 실패와 구분 |

필수 로그 위치는 `/var/log/b3-1-bootstrap.log`, `/var/log/cloud-init-output.log`, `/var/log/nginx/access.log`입니다. 보너스는 `/var/log/b3-1-bonus-bootstrap.log`와 `sudo docker logs b3-1-bonus-web`을 확인합니다. 실제 장애·복구 결과는 [troubleshooting.md](troubleshooting.md)에 보존했습니다.

권한 변경이 필요하면 거부된 API·자원 ARN·리전·요청 시각과 필요한 목적을 기록하고 현재 정책의 조건부터 확인합니다. 계정 소유자가 필요한 Action·Resource·Condition·사용 기간을 검토·승인한 뒤 최소 범위만 변경합니다. 변경 전후 JSON, 승인 시각, 검증·원복 결과를 비밀정보 없이 남깁니다. 이번에는 보너스용 권한 확대 없이 기존 정책을 사용했습니다. AdministratorAccess를 복구 수단으로 추가하지 않습니다.

## 4. 병목 진단과 확장 기준 — 향후 계획

아래 수치는 교육용 초기 판단선입니다. 실제 관측값·부하 시험 결과·확정 SLA가 아닙니다. 같은 요청으로 지표를 함께 확인하고 원인을 좁힙니다.

| 병목 후보 | 확인할 지표·수단 | 계획한 판단과 대응 |
|---|---|---|
| CPU·크레딧 | CPUUtilization, CPUCreditBalance·Usage, `top` | CPU 70% 이상이 10분 지속되거나 크레딧 고갈과 지연이 겹치면 프로세스·요청량 조사 후 최적화·사양 변경 검토 |
| 메모리 | `free -m`, 프로세스 RSS, OOM 로그 | 메모리 80% 초과 지속 또는 OOM이면 누수·작업 크기 확인, 메모리 증설 필요성 검토 |
| 디스크·I/O | `df -h`, `vmstat`, EBS 지표 | 사용률 80% 초과 또는 대기 증가 시 로그·파일 증가 원인과 보관 정책 점검 |
| 요청 처리 | 접근 로그, 별도 부하 시험의 p95 지연·5xx 비율, NetworkIn/Out | p95 500 ms 초과 또는 5xx 1% 초과가 10분 지속되면 서버·네트워크·요청 유형을 대조 |
| 가용성 | 상태 검사·프로세스 종료·재시작 관찰 | 서버 한 대의 장애로 서비스를 중단할 수 없는 요구가 생기면 다중 서버 설계 검토 |

EC2 기본 지표와 에이전트 수집 지표를 구분합니다. 메모리·파일시스템 사용률은 기본 EC2 지표로 수집됐다고 가정하지 않습니다. 위 시계열·알람·CloudWatch 에이전트는 이번에 구성하지 않았습니다. 현재 실습 IAM의 CloudWatch 조회 권한도 추가하지 않았습니다. [EC2 지표](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/viewing_metrics_with_cloudwatch.html), [에이전트 수집 지표](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/metrics-collected-by-CloudWatch-agent.html).

**ALB 도입 조건:** 단일 서버 최적화 후에도 필요한 처리량을 충족하지 못해 서버 두 대 이상으로 분산해야 하거나, 서버 장애·배포 중에도 서비스를 계속해야 할 때 검토합니다. 원인 측정 → 개선 → 같은 부하로 재측정 → 비용·가용성 비교 순서로 결정합니다.

도입 시 서울의 서로 다른 두 AZ에 ALB용 Subnet을 준비하고 대상 서버·Target Group·/health 검사를 구성하는 방안을 검토합니다. EC2 웹 포트의 소스를 ALB SG로 제한하고, 공용 ALB의 HTTPS 입구와 내부 서버를 분리합니다. ALB만 추가한 단일 대상 서버 구성으로 서버 장애 대응이 완성됐다고 판단하지 않습니다. 현재 과제에서는 micro 한 대의 정적 페이지 검증으로 충분해 ALB를 만들지 않았습니다. [ALB의 역할](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html), [AZ·Subnet 조건](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html#subnets-load-balancer).

## 5. 자원 이름·비용 추적·대응

실제 태그는 `Project=b3-1`, `Name=b3-1-...`입니다. 보너스 자원에는 `b3-1-bonus-<역할>` 접두사를 사용했습니다. 예: `b3-1-bonus-vpc`, `b3-1-bonus-igw`, `b3-1-bonus-rtb-public`, `b3-1-bonus-web-sg`, `b3-1-bonus-web`, `b3-1-bonus-key`. Public Subnet 이름은 `b3-1-bonus-subnet-public1-ap-northeast-2a`입니다. EC2·루트 볼륨·ENI에도 Project 태그를 적용했고, VPC 자동 생성 기본 자원은 상위 VPC의 종속 자원으로 추적했습니다.

`resources.json`과 `bonus-resources.json`의 ID·생성/종료 시각·삭제 상태를 함께 대조합니다. Name은 운영자의 식별 규칙이며, IAM의 Project 태그 조건과 구분합니다. 비용 배분 보고서는 태그를 붙인 뒤 Billing에서 비용 할당 태그 활성화가 필요합니다. 이번 계정에서 활성화·비용 집계를 확인했다고 기록하지 않습니다. [AWS 비용 할당 태그](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html).

| 비용 요인 | 추적·예방·대응 |
|---|---|
| EC2 실행 시간·CPU 크레딧 | micro 한 대와 Standard 모드 사용, 실행 구간 기록, 검증 후 종료 |
| EBS·스냅샷 | gp3 8 GiB, 종료 시 삭제. 미사용 볼륨 목록 확인, 스냅샷 생성 시 별도 정리 대상으로 등록 |
| 공인 IPv4·Elastic IP | 자동 할당 IP 한 개, 종료 후 반환 확인. EIP는 미생성·잔여 0개 확인 |
| 데이터 전송·로그 저장 | 소규모 검증 요청만 수행. 재운영 시 트래픽·로그 보관량 증가 확인 |
| NAT·ALB·RDS | 이번에는 미생성. 향후 도입 시 시간·처리량·스토리지 비용과 정리 항목을 추가해 사전 비교 |

사전 비용은 실행 시간×EC2 단가, IPv4 사용 시간×주소 단가, EBS 용량×보관 기간에 해당 단가를 적용하고 전송·추가 서비스 비용을 합산해 추정합니다. 무료 플랜·크레딧 적용 후의 실제 청구액은 Billing에서 별도로 확인합니다. 자원 삭제와 청구액 0달러를 같은 결과로 기록하지 않습니다.

재운영 시 계정 소유자에게 Billing 조회·Project 비용 배분과 소액 예산 알림 설정을 요청합니다. 예시 기준은 월 실제/예측 지출 1달러이며, 승인 전에는 생성하지 않습니다. AWS Budgets에는 비용 반영·통지 지연이 있어 즉시 차단 장치로 사용하지 않습니다. [AWS 예산의 갱신·통지 지연](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html).

예상 밖 사용량·크레딧 감소·비용 알림이 보이면 계정·기간·리전·서비스별 사용량 확인 → 태그와 자원 ID 대조 → 불필요한 실행·자동 확장 중지 → 필요한 증빙 확보 → 소유자가 확인한 실습 자원 정리 → 비용 반영 후 재조회 순으로 대응합니다. 운영에 필요한 기존 자원은 정리 대상에서 구분합니다.

**실제 확인 범위:** 2026-10-19와 10-21의 EC2·EBS·IP·실습 네트워크 삭제를 확인했습니다. Billing 최종 청구액·현재 크레딧 잔액·예산 알림 설정은 미확인입니다. 권한이 없는 실습 사용자의 완료 항목으로 표시하지 않습니다. 실제 정리 근거는 [cleanup-checklist.md](cleanup-checklist.md)에 있습니다.
