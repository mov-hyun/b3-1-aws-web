# 외부 검증 방식과 브라우저 관찰 기록

## 필수 제출 방식: B

과제 원문의 외부 접속 검증은 **“외부 접속 검증(택 1)”**, **“아래 방식 중 1개”**입니다. A는 공인 IP를 브라우저로 여는 방식이고, B는 공인 IP의 /health에 GET 요청을 보내는 방식입니다. 이 저장소의 필수 제출 방식은 B입니다.

| 실습 | 실제 외부 요청 | 시각(KST) | 결과·원본 |
|---|---|---|---|
| 필수 | GET http://3.36.67.14/health | 2026-10-19 19:37:35 | 200·OK, [원본 로그](logs/external-health.txt) |
| 보너스 | GET http://3.34.131.100/health | 2026-10-21 12:53:39~40 | 200·OK, [원본 로그](logs/bonus-external-verification.txt) |

B를 선택한 이유는 URL·응답 상태·고정 본문·검증 시각을 명령 출력으로 함께 보관할 수 있기 때문입니다. 당시 생성한 본인 EC2의 현재 공인 IP를 확인하고, VPC 외부의 학습자 PC에서 요청한 결과입니다.

10월 19일 브라우저의 공인 IP 직접 열기에서는 `ERR_BLOCKED_BY_CLIENT`가 관찰됐습니다. 당시 관찰은 [evidence.md](evidence.md)에 기록했고 A 성공으로 제출하지 않았습니다. curl의 외부 HTTP 성공은 별도 원본 로그로 확인했습니다.

## 2026-10-21 보너스의 실제 HTTPS 브라우저 확인

아래는 배포 당시 브라우저에서 확인한 URL·제목·본문을 정리한 관찰 기록입니다. 자동 평가에서 제외되는 이미지의 설명을 텍스트로 함께 제공합니다.

| 항목 | 관찰 결과 |
|---|---|
| 연 URL | https://bonus-movhyun.3.34.131.100.sslip.io/ |
| 페이지 제목 | Hello Cloud · Codyssey B3-1 |
| 제목 표시 | Hello Cloud. |
| 서버 설명 | 이 페이지는 Caddy (Docker)가 제공하는 정적 페이지입니다. |
| 요청 경로 표시 | 외부 브라우저 → Internet Gateway → Public Subnet의 EC2 → Caddy (Docker) |
| OS·웹 서비스 표시 | Amazon Linux 2023 + Caddy (Docker) |
| 상태 확인 링크 | /health를 열어 본문 OK 표시 확인 |
| 인증서 | 보안 경고 우회 없이 페이지 표시. 별도 curl·Python 신뢰 CA/호스트 이름 검사도 통과 |
| 저장한 화면 | [실제 HTTPS 페이지 PNG](screenshots/bonus-https-page.png) |

확인 절차는 HTTPS 루트 URL 열기 → Hello Cloud와 서버 설명 표시 확인 → GET /health 링크 열기 → 본문 OK 확인 → 화면 저장입니다. 별도 외부 HTTP·HTTPS 검증에서는 200·OK, TLS 검증 결과 0과 TLS 1.3을 확인했습니다. 인증서·응답 원문은 [외부 검증 로그](logs/bonus-external-verification.txt)에 있습니다.

필수 제출 방식은 B로 유지합니다. 보너스 HTTPS 브라우저 화면은 추가 증빙입니다. 두 실습의 서버와 공인 IP는 정리·반환했으므로 현재 주소를 새로 열어 재검증하지 않습니다. 현재 제출물은 보관된 실행 로그·관찰 기록·PNG입니다.
