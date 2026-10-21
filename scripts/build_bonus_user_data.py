"""Prepare one AL2023 Docker/Caddy lab instance; never calls AWS locally."""

from pathlib import Path
from build_user_data import heredoc

ROOT = Path(__file__).resolve().parents[1]


def build_script(html: str, caddyfile: str) -> str:
    script = """#!/bin/bash
set -euo pipefail
exec > >(tee -a /var/log/b3-1-bonus-bootstrap.log) 2>&1
command -v curl >/dev/null || dnf install -y curl-minimal
TOKEN=$(curl --fail --silent --show-error --connect-timeout 3 --max-time 10 -X PUT -H 'X-aws-ec2-metadata-token-ttl-seconds: 300' http://169.254.169.254/latest/api/token)
PUBLIC_IP=$(curl --fail --silent --show-error --connect-timeout 3 --max-time 10 -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/public-ipv4)
SITE_DOMAIN="bonus-movhyun.${PUBLIC_IP}.sslip.io"
unset TOKEN
dnf install -y docker
systemctl enable --now docker
install -d -m 755 /opt/b3-1-bonus/site
"""
    # Preserve the original Nginx page; this is the container lab's derived copy.
    bonus_html = html.replace("Nginx", "Caddy (Docker)")
    script += heredoc("/opt/b3-1-bonus/site/index.html", bonus_html, "B31_BONUS_HTML_END")
    script += heredoc("/opt/b3-1-bonus/Caddyfile", caddyfile, "B31_BONUS_CADDY_END")
    script += """printf '%s\\n' "$SITE_DOMAIN" > /opt/b3-1-bonus/domain.txt
docker pull caddy:2-alpine
CADDY_IMAGE=$(docker image inspect caddy:2-alpine --format '{{index .RepoDigests 0}}')
printf '%s\\n' "$CADDY_IMAGE" > /opt/b3-1-bonus/image-digest.txt
docker volume create b3-1-bonus-caddy-data
docker volume create b3-1-bonus-caddy-config
docker run --rm --env SITE_DOMAIN="$SITE_DOMAIN" \
    --mount type=bind,src=/opt/b3-1-bonus/Caddyfile,dst=/etc/caddy/Caddyfile,readonly \
    "$CADDY_IMAGE" caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile
docker run --detach --name b3-1-bonus-web --restart unless-stopped \
    --publish 80:80 --publish 443:443 \
    --env SITE_DOMAIN="$SITE_DOMAIN" \
    --mount type=bind,src=/opt/b3-1-bonus/site,dst=/srv,readonly \
    --mount type=bind,src=/opt/b3-1-bonus/Caddyfile,dst=/etc/caddy/Caddyfile,readonly \
    --mount type=volume,src=b3-1-bonus-caddy-data,dst=/data \
    --mount type=volume,src=b3-1-bonus-caddy-config,dst=/config \
    "$CADDY_IMAGE"
curl --fail --silent --show-error --retry 12 --retry-all-errors --retry-delay 2 --retry-max-time 45 --max-time 10 http://localhost/health
docker ps --filter name=b3-1-bonus-web
printf 'Bonus HTTPS domain: %s\\n' "$SITE_DOMAIN"
"""
    if len(script.encode("utf-8")) > 16_384:
        raise ValueError("EC2 raw user data must fit within 16 KiB")
    return script


if __name__ == "__main__":
    script = build_script(
        (ROOT / "site" / "index.html").read_text(encoding="utf-8"),
        (ROOT / "bonus" / "Caddyfile").read_text(encoding="utf-8"),
    )
    output = ROOT / ".local" / "bonus-user-data.sh"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(script, encoding="utf-8", newline="\n")
    print(f"Prepared {output} ({len(script.encode('utf-8'))} bytes); no AWS resources created.")
