# 아키텍처와 요청·응답 경로

2026-10-19 필수 실습의 실제 구성을 텍스트로 정리했습니다. 제출용 [architecture.png](architecture.png)와 함께 읽습니다. 이미지가 제외되는 자동 평가에서도 구성·연결·트래픽 방향을 확인할 수 있도록 같은 내용을 Markdown에 남깁니다. 아래 식별자는 모두 삭제 전 기록입니다.

## 필수 실습 구성

```text
External client -- HTTP TCP 80 --> Internet Gateway
                                   igw-0d74537870ddac231
                                           |
                  VPC vpc-03e10d298aa4cfe69 (10.31.0.0/16)
                                           |
                    Public Subnet (10.31.1.0/24, ap-northeast-2a)
                    subnet-079fb16d7994f562e
                                           |
                    EC2 i-0f0e25192b43a666e + Security Group
                    public IPv4 3.36.67.14 -> private 10.31.1.236
                    Nginx :80 -> GET /health -> 200 OK / OK
                    encrypted gp3 EBS 8 GiB

Subnet -- explicit association --> Route Table rtb-096d76633cf668831
                                   10.31.0.0/16 -> local
                                   0.0.0.0/0    -> igw-0d74537870ddac231

Response: EC2 -> subnet routing -> IGW -> external client
Admin: learner public IP /32 -- SSH TCP 22 --> same EC2
Control: b3-1-lab + MFA -- authorized AWS API actions --> lab resources
```

| 구성 요소 | 역할과 실제 설정 |
|---|---|
| VPC | 실습 자원의 네트워크 경계. CIDR 10.31.0.0/16 |
| Public Subnet | EC2가 배치된 주소 범위. 별도 Route Table과 명시적으로 연결 |
| Route Table | VPC 내부 목적지는 local, 나머지 IPv4 목적지는 IGW로 보내는 경로 선택 |
| Internet Gateway | VPC와 인터넷 연결. 공인 IPv4와 EC2의 사설 IPv4 사이의 변환 제공 |
| Security Group | EC2 네트워크 인터페이스에 적용하는 방화벽. 인바운드 80은 전체 IPv4, 22는 학습자 IP /32 |
| EC2·EBS | t3.micro에서 Nginx 실행. 암호화된 gp3 8 GiB 루트 볼륨, 종료 시 삭제 |
| IAM | 사용자에게 AWS 자원의 생성·조회·정리 권한 부여. 웹 요청의 패킷 경로와 별도로 관리 |

## 외부 요청이 도착하는 조건

IGW가 VPC에 연결되고 Subnet의 경로표에 `0.0.0.0/0 → IGW`가 있어야 합니다. EC2에는 공인 IPv4가 필요하고, SG가 요청 포트를 허용하며, 서버가 해당 포트에서 실행돼야 합니다. `0.0.0.0/0` 경로만 추가했다고 모든 포트가 허용되는 것은 아닙니다. 이 관계는 [AWS 인터넷 게이트웨이 문서](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html)에 근거합니다.

실제 검증은 SSH 접속, Nginx active·enabled, localhost 200, 외부 공인 IP의 /health 200·OK, 외부 HTTPS 요청 200입니다. 원본은 [evidence.md](evidence.md)와 [서버 로그](logs/server-verification.txt)에 있습니다.

## 보너스 실습에서 달라진 부분

2026-10-21에는 별도 VPC·EC2에서 같은 형태의 네트워크를 다시 구성했습니다. Nginx 대신 Docker의 Caddy를 사용했고, TCP 80:80과 443:443을 매핑했습니다. 무료 서브도메인으로 HTTPS 인증서를 검증했습니다.

| 항목 | 보너스 실제 값 |
|---|---|
| VPC·Subnet | vpc-004d02de3da12a529 · subnet-00f11a9f0ebce0473 |
| 경로표·IGW | rtb-0df7c8ad8b088e88c의 0.0.0.0/0 → igw-07cffc3e7fc836831 |
| EC2·공인 IP | i-082daaa8d2788b50a · 3.34.131.100 |
| HTTP | 외부 공인 IP → TCP 80 → Caddy 컨테이너 → /health 200·OK |
| HTTPS | bonus-movhyun.3.34.131.100.sslip.io → TCP 443 → Caddy 컨테이너 → 인증서 검증·/health 200·OK |

두 실습의 EC2·EBS·IP·실습 네트워크는 모두 정리했습니다. [필수 자원 기록](resources.json), [보너스 자원 기록](bonus-resources.json), [정리 근거](cleanup-checklist.md)를 함께 확인합니다. 반환된 공인 IP에 새 요청을 보내지 않습니다.
