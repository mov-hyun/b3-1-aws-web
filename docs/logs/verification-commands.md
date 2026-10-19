# 검증 당시 실행 명령

2026-10-19 배포 검증에 사용한 명령 기록입니다. 서버 종료와 공인 IP 반환을 완료했으므로 아래 과거 IP로 다시 실행하지 않습니다. 재배포할 때는 본인 새 인스턴스의 IP·키 페어·검증한 호스트 키로 대체합니다. 개인키와 known_hosts는 .local/에 별도 보관합니다.

```powershell
ssh.exe -i .local/b3-1-web-key.pem -o IdentitiesOnly=yes -o BatchMode=yes `
  -o StrictHostKeyChecking=yes -o UserKnownHostsFile=.local/known_hosts `
  ec2-user@3.36.67.14 `
  'date -u; hostname; id -un; sudo systemctl is-active nginx; sudo systemctl is-enabled nginx; sudo nginx -t; curl --fail --silent --show-error -i http://localhost/health; curl --fail --silent --show-error -o /dev/null -w "localhost HTTP %{http_code}\n" http://localhost; curl --fail --silent --show-error -o /dev/null -w "outbound HTTPS %{http_code}\n" https://example.com'

curl.exe --noproxy '*' --fail --silent --show-error -i http://3.36.67.14/health
```
