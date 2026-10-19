# 트러블슈팅 보고서

현재 상태: **MFA 로그인 문제와 Nginx 배포 문제 해결, 서버 내부·외부 검증 완료**.

## 사례 1 — MFA 등록 표시 후 과제용 사용자 재로그인 실패 (해결)

| 항목 | 실제 관찰·근거 |
|---|---|
| 증상 | 2026-10-19 `b3-1-lab`에 `Passkey MFA device assigned`, MFA `(1)`이 표시됐지만 재로그인에서 사용할 패스키를 사용자가 확인하지 못했습니다. 이후 로그인 화면에서 패스키 인증 취소 오류가 표시됐습니다. |
| 원인 가설 | 등록된 공개키에 대응하는 인증수단의 저장 위치나 사용 방법을 확인하지 못한 상태일 수 있습니다. 등록 성공 표시만 확인하고 실제 재로그인 가능 여부를 검증하지 않은 것이 안내 과정의 문제였습니다. 구체적인 저장 위치·기기·직접 원인은 미확인입니다. |
| 검증 | 최초에는 `인증 정보가 정확하지 않습니다`가 표시됐습니다. 이후 새 비밀번호 입력을 통과해 `추가 확인 필요`, `패스키 또는 보안 키로 보호됩니다` 단계로 이동한 것을 확인했습니다. 그 뒤 `패스키 인증 프로세스를 취소한 것 같습니다`가 표시됐으므로 현재 복구 대상은 MFA입니다. `iam:GetMFADevice` 조회 거부와 로그인용 패스키 부재 문제를 구분했습니다. |
| 조치 | 루트 콘솔 재로그인 후 과제용 사용자의 MFA와 연결 정책을 조회했습니다. 사용자가 직접 인증 앱 MFA `b3-1-lab-app`을 추가했고, AWS에서 등록 성공을 확인했습니다. 이후 사용자가 기존 과제용 패스키를 삭제했습니다. 삭제 성공과 인증 앱 1개 유지 확인 후 루트에서 로그아웃하고 과제용 사용자 로그인 화면을 준비했습니다. |
| 결과 | 2026-10-19 사용자가 인증 앱 코드로 `b3-1-lab` 재로그인을 완료했습니다. 서울 EC2의 인스턴스·볼륨 조회가 성공했고, 이후 같은 MFA 세션에서 VPC·Subnet·IGW·라우팅·보안 그룹과 EC2 한 대 생성까지 성공했습니다. |
| 재발 방지 | MFA 등록 전에 사용할 기기·앱·저장 방식을 정하고, 사용자가 인증수단을 실제로 사용할 수 있는지 확인합니다. 사용자 전환과 인프라 생성 전에 재로그인을 검증합니다. 비밀번호·QR·비밀키·인증 코드는 저장소·로그·채팅에 남기지 않습니다. |

비공개 확인 화면은 Git 제외 경로 `.local/proof/`의 `lab-app-only.png`, `lab-ec2-read-success.png`, `ec2-launched.png`에 보관했습니다. QR·비밀키·인증 코드는 저장하지 않았습니다.

공식 복구 안내: https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_mfa-fido.html

## 사례 2 — curl 패키지 충돌로 Nginx 설치 중단 (해결)

| 항목 | 실제 관찰·근거 |
|---|---|
| 증상 | 2026-10-19 19:34 KST EC2 생성 후 외부 TCP 80 접속 실패. 19:36 KST SSH는 성공했지만 `systemctl is-active nginx`는 `inactive`였습니다. |
| 원인 가설 | user-data의 패키지 설치 단계가 실패해 Nginx를 실행하지 못했을 수 있습니다. |
| 검증 | `/var/log/b3-1-bootstrap.log`에 `curl-minimal ... conflicts with curl provided by curl`을 확인했습니다. `/var/log/cloud-init-output.log`에는 10:36:22 UTC `Failed to run module scripts-user`가 남았습니다. AL2023 기본 `curl-minimal`과 `dnf install -y nginx curl`이 충돌했고 `set -e`로 후속 설정이 중단됐습니다. SSH 성공, IGW 기본 경로 Active, SG 80 규칙 존재도 확인했습니다. |
| 조치 | 실패 로그를 보존했습니다. `scripts/build_user_data.py`에서 Nginx만 설치하고, `command -v curl`이 실패할 때만 `curl-minimal`을 설치하도록 수정했습니다. 재생성한 스크립트를 SCP로 같은 EC2에 전송하고 `sudo bash /home/ec2-user/b3-1-deploy.sh`로 실행했습니다. |
| 결과 | 스크립트 종료 코드 0. `nginx -t` 성공, 서비스 `active`·`enabled`, localhost `/` 200 및 `/health` 200·`OK`, 아웃바운드 HTTPS 200 확인. 19:37:35 KST 외부 `http://3.36.67.14/health`도 200·`OK`였습니다. |
| 재발 방지 | AMI 기본 패키지를 확인하고 불필요한 패키지 교체를 피합니다. 배포 후 cloud-init 로그, 서비스 상태, localhost, 외부 접속 순으로 확인합니다. Bash 문법 검사만으로 실제 설치 성공을 판단하지 않습니다. 수정된 user-data를 재배포 기준으로 사용합니다. |

원본 근거: [초기 오류와 복구 로그](logs/bootstrap-troubleshooting.txt), [서버 검증](logs/server-verification.txt), [외부 응답](logs/external-health.txt).

AWS 공식 문서: [AL2023의 curl / libcurl 패키지 구성](https://docs.aws.amazon.com/linux/al2023/ug/curl-minimal.html).
