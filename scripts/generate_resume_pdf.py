from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "resume" / "bongjae-choi-resume.pdf"
FONT_PATH = Path("/System/Library/Fonts/Supplemental/AppleGothic.ttf")

PAGE_W, PAGE_H = A4
LEFT = 42
RIGHT = PAGE_W - 42
TOP = PAGE_H - 42
BOTTOM = 42

INK = colors.HexColor("#17212f")
TEXT = colors.HexColor("#2f3b49")
MUTED = colors.HexColor("#66717d")
LINE = colors.HexColor("#d8dde3")
SOFT = colors.HexColor("#f6f7f8")
ACCENT = colors.HexColor("#1f6f8b")


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("AppleGothic", str(FONT_PATH)))


def text_width(text: str, size: float) -> float:
    return pdfmetrics.stringWidth(text, "AppleGothic", size)


def wrap_text(text: str, width: float, size: float) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if text_width(candidate, size) <= width:
            current = candidate
            continue
        if current:
            lines.append(current)
            current = word
        else:
            lines.append(word)
            current = ""
    if current:
        lines.append(current)
    return lines


def draw_text(c: canvas.Canvas, text: str, x: float, y: float, size: float = 9.5, color=TEXT) -> None:
    c.setFillColor(color)
    c.setFont("AppleGothic", size)
    c.drawString(x, y, text)


def draw_right(c: canvas.Canvas, text: str, x: float, y: float, size: float = 9.5, color=TEXT) -> None:
    c.setFillColor(color)
    c.setFont("AppleGothic", size)
    c.drawRightString(x, y, text)


def draw_rule(c: canvas.Canvas, y: float, color=LINE, width: float = 0.7) -> None:
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(LEFT, y, RIGHT, y)


def draw_section(c: canvas.Canvas, title: str, y: float) -> float:
    draw_text(c, title, LEFT, y, 12.2, INK)
    draw_rule(c, y - 5)
    return y - 17


def draw_wrapped(
    c: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    width: float,
    size: float = 9.4,
    leading: float = 13.2,
    color=TEXT,
) -> float:
    for line in wrap_text(text, width, size):
        draw_text(c, line, x, y, size, color)
        y -= leading
    return y


def draw_bullets(c: canvas.Canvas, bullets: list[str], x: float, y: float, width: float, size: float = 9.15) -> float:
    bullet_gap = 10
    leading = 12.4
    for item in bullets:
        lines = wrap_text(item, width - bullet_gap, size)
        draw_text(c, "•", x, y, size, INK)
        for idx, line in enumerate(lines):
            draw_text(c, line, x + bullet_gap, y - idx * leading, size, TEXT)
        y -= leading * len(lines) + 1.5
    return y


def draw_header(c: canvas.Canvas) -> float:
    y = TOP
    draw_text(c, "최봉재", LEFT, y - 2, 26, INK)
    draw_text(c, "(Bongjae Choi)", LEFT + 82, y + 1, 18, INK)
    draw_right(c, "Senior App / Cross-Platform Engineer", RIGHT, y + 2, 10.5, ACCENT)

    y -= 24
    draw_rule(c, y, INK, 0.9)
    y -= 17

    x = LEFT
    parts = [
        ("010-5852-4678", None),
        ("jjgod0124@gmail.com", None),
        ("Portfolio: bongjaechoi.github.io", "https://bongjaechoi.github.io/"),
        ("GitHub: github.com/BongJaeChoi", "https://github.com/BongJaeChoi"),
    ]
    for label, url in parts:
        draw_text(c, label, x, y, 8.9, MUTED if url is None else INK)
        w = text_width(label, 8.9)
        if url:
            c.linkURL(url, (x, y - 2, x + w, y + 10), relative=0, thickness=0, color=None)
        x += w + 12
    return y - 25


def draw_strengths(c: canvas.Canvas, y: float) -> float:
    y = draw_section(c, "Core Strengths", y)
    col_w = (RIGHT - LEFT - 18) / 3
    items = [
        (
            "Mobile Product Engineering",
            "Flutter, Android, 앱 생명주기, 스토어 배포, 하이브리드 앱 운영 경험",
        ),
        (
            "WebView / Payment / Auth",
            "앱과 웹 사이의 인증, PG 결제 예외, 딥링크, 세션 경계 문제 정리",
        ),
        (
            "AI-assisted Guardrails",
            "AI 작업 지침, 위험 패턴 차단, 서브에이전트 분업, 배포 전 검증 루틴",
        ),
    ]
    for idx, (title, body) in enumerate(items):
        x = LEFT + idx * (col_w + 9)
        c.setFillColor(SOFT)
        c.rect(x, y - 57, col_w, 58, fill=1, stroke=0)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.4)
        c.rect(x, y - 57, col_w, 58, fill=0, stroke=1)
        draw_text(c, title, x + 7, y - 13, 8.8, ACCENT)
        draw_wrapped(c, body, x + 7, y - 28, col_w - 14, 8.1, 10.5, TEXT)
    return y - 72


def draw_skills(c: canvas.Canvas, y: float) -> float:
    y = draw_section(c, "Skills", y)
    rows = [
        ("Mobile", "Flutter, Dart, Android, Kotlin, Java, RxJava, MVVM, Clean Architecture, Jetpack"),
        ("App Boundary", "WebView, JSBridge, Cookie Auth, Deep Link, PG Payment Flow, SignalR, FCM"),
        ("Frontend", "React, Vue, TypeScript, TanStack Query, Zustand"),
        ("Release / Ops", "Fastlane, Firebase App Distribution, CI/CD, Docker, Nginx Reverse Proxy"),
        ("AI Workflow", "AGENTS.md, Copilot Instructions, Cursor, AI Coding Guardrail, verification commands"),
    ]
    label_w = 92
    for label, values in rows:
        draw_text(c, label, LEFT, y, 8.7, INK)
        y = draw_wrapped(c, values, LEFT + label_w, y, RIGHT - LEFT - label_w, 8.45, 11.1, TEXT)
        y -= 1.5
    return y - 5


def draw_job(
    c: canvas.Canvas,
    y: float,
    company: str,
    period: str,
    subtitle: str,
    bullets: list[str] | None = None,
    tech: str | None = None,
    compact: bool = False,
) -> float:
    draw_text(c, company, LEFT, y, 10.4, INK)
    draw_right(c, period, RIGHT, y, 8.8, MUTED)
    y -= 14
    draw_text(c, subtitle, LEFT, y, 9.0, INK)
    y -= 13
    if bullets:
        y = draw_bullets(c, bullets, LEFT + 2, y, RIGHT - LEFT - 2, 8.65 if compact else 8.85)
    if tech:
        y -= 1
        y = draw_wrapped(c, tech, LEFT, y, RIGHT - LEFT, 8.1, 10.2, MUTED)
    return y - 9


def page_one(c: canvas.Canvas) -> None:
    y = draw_header(c)

    y = draw_section(c, "Summary", y)
    summary = (
        "Flutter와 Android 기반 앱 개발 경험을 중심으로, WebView 인증, 결제 예외, 실시간 상태, "
        "앱 배포 자동화처럼 제품 운영에서 자주 깨지는 경계를 정리해 온 모바일 중심 제품 엔지니어입니다. "
        "AI 도구는 단순 코드 생성이 아니라 AGENTS.md, Copilot instructions, 테스트/검증 명령으로 결과를 확인하는 "
        "개발 루틴으로 사용합니다."
    )
    y = draw_wrapped(c, summary, LEFT, y, RIGHT - LEFT, 9.25, 12.8, TEXT) - 6

    y = draw_strengths(c, y)
    y = draw_skills(c, y)

    y = draw_section(c, "Experience", y)
    y = draw_job(
        c,
        y,
        "실시간 예약 협상 플랫폼 개발 (Dealert)",
        "2025.07 - 2026.04",
        "Flutter 앱 2종과 React 파트너 웹의 결제, 인증, 실시간, 배포 흐름 안정화",
        [
            "PG/WebView/앱 라우팅 경계에서 결제 취소 상태를 성공/실패 흐름과 분리하고 테스트로 고정했습니다.",
            "WebView 쿠키 인증, 자동 로그인 의도, 토큰 갱신 순서를 나눠 로그인 풀림 회귀를 줄였습니다.",
            "Fastlane/Firebase App Distribution 기반 iOS·Android 병렬 배포로 순차 빌드 대비 약 50% 시간을 절약했습니다.",
            "SignalR 기반 실시간 딜/예약 상태 업데이트와 자동 재연결 흐름을 앱과 웹 양쪽에서 정리했습니다.",
            "AGENTS.md, Copilot instructions, React/Flutter 위험 패턴 문서와 검증 명령으로 AI 작업 결과를 확인했습니다.",
        ],
        "Flutter, Dart, React, TypeScript, WebView, SignalR, Fastlane, Firebase, Nginx",
    )

    draw_job(
        c,
        y,
        "주식회사 루나소프트 / 그린앤그레이",
        "2021.05 - 2024.05",
        "버티컬 패션 쇼핑몰 셀룩 하이브리드 앱 및 Vue 프론트엔드 개발",
        [
            "Vue 기반 프론트엔드 초기 프로젝트 구조와 빌드 세팅을 구성했습니다.",
            "JSBridge 인터페이스로 Native App과 Web 간의 유기적 통신을 구현했습니다.",
            "React Query, TypeScript, API 문서 기반 코드 생성 흐름을 도입해 반복 구현 비용을 줄였습니다.",
            "배포 시스템과 QA 프로세스를 정리해 릴리즈 안정성을 높였습니다.",
        ],
        "Vue, TypeScript, JSBridge, Hybrid App, React Query",
        compact=True,
    )


def page_two(c: canvas.Canvas) -> None:
    y = TOP
    y = draw_section(c, "Experience Continued", y)
    y = draw_job(
        c,
        y,
        "(주)피알앤디컴퍼니 (헤이딜러)",
        "2018.10 - 2020.12",
        "중고차 플랫폼 헤이딜러 고객용/딜러용 Android 앱 개발",
        [
            "딜러 전용 앱 리뉴얼(v3 -> v4)에 참여하고 주요 화면과 사용자 흐름을 구현했습니다.",
            "이미지 첨부 프로세스의 메모리 문제를 Stream 기반 처리로 개선해 앱 안정성과 UX를 높였습니다.",
            "Kotlin 도입과 MVVM 기반 안드로이드 아키텍처 적용을 진행했습니다.",
        ],
        "Android, Kotlin, Java, RxJava, MVVM, Image Pipeline",
    )
    y = draw_job(
        c,
        y,
        "(주)스펙업애드",
        "2018.03 - 2018.09",
        "보상형 앱 타임스프레드 개발",
        ["상점 화면 등 주요 기능을 개발하고 앱 배포 자동화 프로세스를 구축했습니다."],
        compact=True,
    )
    y = draw_job(
        c,
        y,
        "(주)씨이랩",
        "2017.02 - 2018.03",
        "리워드 서비스 치즈카운터 개발",
        ["카메라 및 이미지 처리 기능을 개발하고 네트워크 통신 아키텍처를 설계했습니다."],
        compact=True,
    )
    y = draw_job(
        c,
        y,
        "주식회사 트램스",
        "2015.07 - 2016.07",
        "다수의 Android 앱 외주 및 자체 서비스 개발",
        [
            "식당 매물중개 서비스 앱 초기 설계와 지도 API 연동을 구현했습니다.",
            "통화 화면 커스터마이징, 강연 앱, 물류 PDA 앱 등 다양한 Android 도메인을 개발했습니다.",
        ],
        compact=True,
    )
    y = draw_job(
        c,
        y,
        "주식회사 애니웨어",
        "2014.03 - 2014.08",
        "Android 앱 개발 실무 참여",
    )

    y = draw_section(c, "Education", y - 5)
    draw_text(c, "한국방송통신대학교", LEFT, y, 9.1, INK)
    draw_text(c, "컴퓨터과학과 (2019.03 - 2023.02)", LEFT + 118, y, 9.1, TEXT)
    y -= 15
    draw_text(c, "대전보건대학교", LEFT, y, 9.1, INK)
    draw_text(c, "바이오정보과 (2010.03 - 2014.02)", LEFT + 118, y, 9.1, TEXT)


def main() -> None:
    register_fonts()
    c = canvas.Canvas(str(OUTPUT), pagesize=A4)
    c.setTitle("최봉재 이력서")
    c.setAuthor("Bongjae Choi")
    page_one(c)
    c.showPage()
    page_two(c)
    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    main()
