"""Build an EC2 user-data script locally; this script does not call AWS."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def heredoc(path: str, content: str, delimiter: str) -> str:
    if delimiter in content.splitlines():
        raise ValueError("Source contains the shell here-document delimiter")
    return f"cat > {path} <<'{delimiter}'\n{content.rstrip()}\n{delimiter}\n"


def build_script(html: str, nginx: str) -> str:
    script = """#!/bin/bash
set -euo pipefail
exec > >(tee -a /var/log/b3-1-bootstrap.log) 2>&1
# AL2023 already provides curl-minimal; installing full curl causes a conflict.
dnf install -y nginx
command -v curl >/dev/null || dnf install -y curl-minimal
"""
    script += heredoc("/usr/share/nginx/html/index.html", html, "B31_HTML_END")
    script += heredoc("/etc/nginx/conf.d/b3-1.conf", nginx, "B31_NGINX_END")
    # AL2023 includes a default server in nginx.conf; replace it with our one server.
    script += """cat > /etc/nginx/nginx.conf <<'B31_MAIN_END'
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /run/nginx.pid;
events { worker_connections 256; }
http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    access_log /var/log/nginx/access.log;
    sendfile on;
    keepalive_timeout 30;
    include /etc/nginx/conf.d/*.conf;
}
B31_MAIN_END
nginx -t
systemctl enable --now nginx
systemctl restart nginx
curl --fail --silent --show-error --retry 5 --retry-connrefused http://localhost/health
"""
    if len(script.encode("utf-8")) > 16_384:
        raise ValueError("EC2 raw user data must fit within 16 KiB")
    return script


if __name__ == "__main__":
    output = ROOT / ".local" / "user-data.sh"
    script = build_script(
        (ROOT / "site" / "index.html").read_text(encoding="utf-8"),
        (ROOT / "nginx" / "b3-1.conf").read_text(encoding="utf-8"),
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(script, encoding="utf-8", newline="\n")
    print(f"Prepared {output} ({len(script.encode('utf-8'))} bytes); no AWS resources created.")
