"""Render the verified lab topology; requires Pillow as a local authoring tool."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONT = Path("C:/Windows/Fonts/malgun.ttf")


def main():
    image = Image.new("RGB", (1800, 1320), "#eef3f8")
    draw = ImageDraw.Draw(image)
    fonts = {size: ImageFont.truetype(str(FONT), size) for size in (23, 26, 30, 36, 48)}

    def text(x, y, value, size=26, fill="#172c42"):
        draw.multiline_text((x, y), value, font=fonts[size], fill=fill, spacing=12)

    def box(rect, fill, outline="#b7c9db"):
        draw.rounded_rectangle(rect, radius=20, fill=fill, outline=outline, width=3)

    def arrow(start, end, color="#2868ae"):
        draw.line([start, end], fill=color, width=6)
        x, y = end
        dx, dy = end[0] - start[0], end[1] - start[1]
        if abs(dx) > abs(dy):
            step = 16 if dx > 0 else -16
            draw.polygon([(x, y), (x-step, y-10), (x-step, y+10)], fill=color)
        else:
            step = 16 if dy > 0 else -16
            draw.polygon([(x, y), (x-10, y-step), (x+10, y-step)], fill=color)

    text(65, 45, "AWS WEB LAB · B3-1", 48)
    text(67, 115, "실제 배포 구성 · 2026-10-19 검증 · 검증 후 자원 삭제 완료", 26, "#365e82")
    box((60, 190, 415, 370), "white")
    text(95, 225, "인터넷 사용자", 36)
    text(95, 290, "HTTP 80 → 공인 IPv4", 23)
    box((60, 430, 415, 640), "white")
    text(95, 465, "학습자 PC", 36)
    text(95, 530, "SSH 22\n현재 내 공인 IP /32", 23)
    box((490, 190, 1735, 1015), "#e1edf8", "#6e9bc7")
    text(525, 220, "서울 리전 · ap-northeast-2", 36)
    box((525, 295, 1700, 980), "#f6faff", "#82a9cc")
    text(560, 320, "VPC · 10.31.0.0/16", 30)
    box((570, 400, 930, 560), "white")
    text(600, 425, "Internet Gateway", 30)
    text(600, 480, "인터넷과 VPC 연결", 23)
    box((1010, 400, 1655, 820), "#e5f4f0", "#75ab9d")
    text(1045, 430, "Public Subnet · 10.31.1.0/24", 26)
    box((1050, 500, 1615, 775), "white", "#669788")
    text(1085, 525, "EC2 + Security Group", 30)
    text(1085, 585, "t3.micro · Amazon Linux 2023\n공인 IPv4: 3.36.67.14\nNginx · GET /health → 200 OK\n80: 전체 허용 / 22: 내 IP만 허용", 23)
    box((570, 635, 930, 800), "#fff9e9", "#d8ba75")
    text(600, 660, "Route Table", 30)
    text(600, 715, "0.0.0.0/0 → IGW", 23)
    box((1050, 845, 1615, 945), "white")
    text(1085, 875, "EBS · gp3 8 GiB · 암호화", 26)
    arrow((415, 290), (570, 455))
    arrow((415, 535), (570, 535))
    arrow((930, 480), (1050, 580))
    draw.line([(750, 635), (750, 560)], fill="#aa8a47", width=4)
    draw.line([(930, 730), (1010, 730)], fill="#aa8a47", width=4)
    draw.line([(1330, 775), (1330, 845)], fill="#669788", width=4)
    text(560, 860, "Subnet을 경로표와 연결\n공인 IPv4와 보안 그룹을 함께 설정", 23)
    box((60, 1060, 1735, 1255), "white")
    text(95, 1085, "관리 경로 · IAM 사용자 b3-1-lab + MFA", 30)
    text(95, 1145, "서울의 필요한 EC2/VPC 작업만 허용 · 관리자 권한 없음 · 실습 후 자원 정리", 26)
    text(95, 1195, "IAM은 글로벌 서비스이며 웹 요청의 통신 경로에 포함되지 않습니다.", 23, "#526678")
    target = ROOT / "docs" / "architecture.png"
    image.save(target)
    print(f"Rendered verified lab architecture: {target}")


if __name__ == "__main__":
    main()
