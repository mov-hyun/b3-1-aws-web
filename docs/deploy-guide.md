# 배포와 검증 순서

이 문서는 필수 실습의 재현 가이드입니다. 실제 실행 결과는 evidence.md에 기록했습니다. 삭제된 과거 주소를 사용하지 않고 새로 생성한 본인 자원의 IP·키·호스트 키를 확인한 뒤 적용합니다.

1. 무료 플랜·크레딧을 확인하고 루트 MFA를 등록합니다. 과제용 최소권한 사용자를 만들고, 사용자 MFA 등록 후 새로 로그인합니다.
2. 서울 `ap-northeast-2`에서 기존 실습 자원이 없는지 확인합니다. 생성할 자원에는 `Project=b3-1`과 `Name=b3-1-...` 태그를 붙입니다.
3. `VPC만` 생성으로 `10.31.0.0/16` VPC 한 개를 만듭니다. 자동 구성 마법사가 NAT Gateway를 추가하지 않도록 합니다.
4. Public Subnet `10.31.1.0/24` 한 개, IGW 한 개, 별도 Route Table 한 개를 생성합니다. IGW를 VPC에 연결하고, Route Table에 `0.0.0.0/0 → IGW`를 추가한 뒤 Subnet과 연결합니다.
5. 보안 그룹을 만듭니다. 인바운드는 TCP 80 `0.0.0.0/0`, TCP 22 `현재 내 공인 IP/32` 두 개로 시작합니다. 아웃바운드는 패키지 설치와 HTTPS 요청이 가능하도록 허용합니다.
6. 키 페어 `b3-1-web-key` 한 개를 준비하고 개인키는 `.local/`에 안전하게 보관합니다. 실습과 관계없는 기존 키를 재사용하지 않습니다.
7. EC2 한 대를 생성합니다. 공식 Amazon Linux 2023 x86_64 AMI, 무료 적용 가능한 `t3.micro`, gp3 8 GiB 암호화, 종료 시 볼륨 삭제, 공인 IPv4 할당, 앞서 만든 Subnet·보안 그룹·키를 선택합니다. CPU 크레딧 옵션은 `Standard`, IMDS는 `V2 only / required`, 상세 모니터링은 사용하지 않습니다. IAM 인스턴스 프로파일은 필요하지 않습니다.
8. EC2 생성 시 인스턴스·볼륨·네트워크 인터페이스에 `Project=b3-1` 태그를 지정합니다. AL2023의 기본 curl-minimal을 유지합니다. `python scripts/build_user_data.py`로 만든 `.local/user-data.sh`를 사용자 데이터에 넣습니다.
9. 인스턴스 실행·초기화 완료를 기다린 뒤 SSH로 접속합니다. SSH 사용자는 `ec2-user`입니다.

```powershell
ssh -i .local/b3-1-web-key.pem ec2-user@<PUBLIC_IP>
```

첫 SSH 접속 전에 EC2 시스템 로그의 호스트 키 지문과 ssh-keyscan 결과를 대조합니다. 일치하는 공개 호스트 키만 별도 known_hosts에 저장하고 StrictHostKeyChecking=yes를 사용합니다. 개인키는 Git 제외 경로에서 본인 계정만 읽도록 제한합니다.

인스턴스 안에서 다음 명령의 실제 출력을 기록합니다.

```bash
systemctl is-active nginx
sudo nginx -t
curl -i http://localhost
curl -i http://localhost/health
curl -I https://example.com
sudo tail -n 40 /var/log/nginx/access.log
sudo tail -n 60 /var/log/b3-1-bootstrap.log
```

학습자 PC 등 인스턴스 외부에서 검증합니다.

```powershell
curl.exe -i --connect-timeout 10 http://<PUBLIC_IP>/health
```

10. URL·IP·검증 시각·200/OK 결과와 스크린샷을 README 및 evidence.md에 기록합니다.

외부 검증은 원문의 A/B 중 하나를 선택합니다. 이번 제출은 B입니다. 브라우저를 추가 확인하려면 새로 배포한 본인 EC2의 `http://<현재 공인 IP>/`를 열어 URL·페이지 문구·시각을 기록하고 캡처합니다. 오류가 나면 오류를 기록한 뒤 라우팅·SG·현재 IP·서버 상태를 확인합니다. 실제 보너스 HTTPS 브라우저 관찰은 [browser-verification.md](browser-verification.md)에 따로 보관했습니다.

11. 실제 장애 또는 명시적으로 계획한 장애 재현 1건을 기록합니다. 의도적으로 재현했다면 그 사실을 명시합니다. 증상·가설·검증·조치·결과·재발방지를 모두 채웁니다.
12. 증빙 확보 후 cleanup-checklist.md 순서로 정리합니다. EC2 중지만으로 끝내지 않고 남은 EBS·공인 IP·네트워크 자원을 확인합니다.

비용 주의: 공인 IPv4에는 크레딧 적용 전 요금이 있으며, EBS는 EC2 중지 중에도 남아 있을 수 있습니다. 무료 플랜을 유지하고 필요 이상의 자원을 생성하지 않습니다.

공개 접근 위험·노출 기간·SG와 IAM의 차이·장애 점검 순서·확장 판단·비용 추적과 대응은 [operations.md](operations.md)에 정리했습니다. ALB·VPN·비용 알림은 해당 문서의 향후 계획이며 실습의 생성 완료 항목이 아닙니다.
