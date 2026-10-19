"""Make a read-only HTML viewer of captured command logs for screenshots."""

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

for name, title in (
    ("external-health", "외부 접속 검증 · 방식 B"),
    ("server-verification", "SSH 서버 내부 검증"),
):
    captured = (ROOT / "docs" / "logs" / f"{name}.txt").read_text(encoding="utf-8-sig")
    target = ROOT / ".local" / "evidence-view" / f"{name}.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        '<!doctype html><html lang="ko"><meta charset="utf-8">'
        '<title>B3-1 실제 명령 실행 기록</title><style>'
        'body{margin:40px;background:#f0f4f8;color:#192d43;font-family:system-ui,"Malgun Gothic",sans-serif}'
        'main{max-width:1000px;margin:auto}h1{font-size:30px}p{line-height:1.7}'
        'pre{background:white;border:1px solid #c9d7e4;border-radius:12px;padding:24px;'
        'font:16px/1.7 Consolas,monospace;white-space:pre-wrap;overflow-wrap:anywhere}'
        '</style><main><p>CODYSSEY B3-1 · AWS ap-northeast-2</p>'
        f'<h1>{escape(title)}</h1>'
        '<p>로컬 PC에서 실제 실행한 명령의 저장 로그입니다. 아래 원문을 읽기 위한 화면이며, '
        '이 화면을 열 때 AWS로 새 요청을 보내지는 않습니다.</p>'
        f'<pre>{escape(captured)}</pre>'
        f'<p>원본: docs/logs/{name}.txt · 실제 배포 IP: 3.36.67.14</p></main>',
        encoding="utf-8",
    )
    print(target)
