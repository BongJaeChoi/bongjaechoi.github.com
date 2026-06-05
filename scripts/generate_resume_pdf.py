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
LEFT = 46
RIGHT = PAGE_W - 46
TOP = PAGE_H - 46

INK = colors.HexColor("#111827")
TEXT = colors.HexColor("#273444")
MUTED = colors.HexColor("#6b7280")
LINE = colors.HexColor("#cfd6df")


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("Resume", str(FONT_PATH)))


def text_width(text: str, size: float) -> float:
    return pdfmetrics.stringWidth(text, "Resume", size)


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


def draw_text(c: canvas.Canvas, text: str, x: float, y: float, size: float, color=TEXT) -> None:
    c.setFont("Resume", size)
    c.setFillColor(color)
    c.drawString(x, y, text)


def draw_center(c: canvas.Canvas, text: str, y: float, size: float, color=TEXT) -> None:
    c.setFont("Resume", size)
    c.setFillColor(color)
    c.drawCentredString(PAGE_W / 2, y, text)


def draw_right(c: canvas.Canvas, text: str, y: float, size: float, color=MUTED) -> None:
    c.setFont("Resume", size)
    c.setFillColor(color)
    c.drawRightString(RIGHT, y, text)


def draw_rule(c: canvas.Canvas, y: float, width: float = 0.65) -> None:
    c.setStrokeColor(LINE)
    c.setLineWidth(width)
    c.line(LEFT, y, RIGHT, y)


def draw_section(c: canvas.Canvas, title: str, y: float) -> float:
    draw_text(c, title, LEFT, y, 11.2, INK)
    draw_rule(c, y - 4)
    return y - 15


def draw_wrapped(
    c: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    width: float,
    size: float = 9.0,
    leading: float = 12.2,
    color=TEXT,
) -> float:
    for line in wrap_text(text, width, size):
        draw_text(c, line, x, y, size, color)
        y -= leading
    return y


def draw_bullets(c: canvas.Canvas, bullets: list[str], y: float, size: float = 8.9) -> float:
    bullet_x = LEFT + 2
    text_x = LEFT + 12
    width = RIGHT - text_x
    leading = 12.0
    for item in bullets:
        lines = wrap_text(item, width, size)
        draw_text(c, "–", bullet_x, y, size, INK)
        for index, line in enumerate(lines):
            draw_text(c, line, text_x, y - index * leading, size, TEXT)
        y -= leading * len(lines) + 1.6
    return y


def draw_label_line(c: canvas.Canvas, label: str, value: str, y: float, size: float = 8.7) -> float:
    draw_text(c, f"{label}:", LEFT, y, size, INK)
    draw_text(c, value, LEFT + 88, y, size, TEXT)
    return y - 11.2


def draw_header(c: canvas.Canvas) -> float:
    y = TOP
    draw_text(c, "최봉재 (Bongjae Choi)", LEFT, y, 21.5, INK)
    y -= 18
    draw_text(c, "Senior App / Cross-Platform Engineer · Mobile-first Product Engineering", LEFT, y, 9.4, MUTED)
    y -= 14

    contact = "010-5852-4678 · jjgod0124@gmail.com · Portfolio: bongjaechoi.github.io · GitHub: github.com/BongJaeChoi"
    draw_text(c, contact, LEFT, y, 8.25, TEXT)

    start_x = LEFT
    portfolio_prefix = "010-5852-4678 · jjgod0124@gmail.com · Portfolio: "
    portfolio_text = "bongjaechoi.github.io"
    github_prefix = portfolio_prefix + portfolio_text + " · GitHub: "
    github_text = "github.com/BongJaeChoi"
    portfolio_x = start_x + text_width(portfolio_prefix, 8.2)
    github_x = start_x + text_width(github_prefix, 8.2)
    c.linkURL(
        "https://bongjaechoi.github.io/",
        (portfolio_x, y - 2, portfolio_x + text_width(portfolio_text, 8.2), y + 9),
        relative=0,
        thickness=0,
        color=None,
    )
    c.linkURL(
        "https://github.com/BongJaeChoi",
        (github_x, y - 2, github_x + text_width(github_text, 8.2), y + 9),
        relative=0,
        thickness=0,
        color=None,
    )

    y -= 13
    draw_rule(c, y, 0.9)
    return y - 17


def draw_job(
    c: canvas.Canvas,
    y: float,
    title: str,
    organization: str,
    period: str,
    bullets: list[str],
    tech: str | None = None,
    size: float = 8.85,
) -> float:
    draw_text(c, title, LEFT, y, 10.0, INK)
    draw_right(c, period, y, 8.6, MUTED)
    y -= 12.2
    draw_text(c, organization, LEFT, y, 8.9, MUTED)
    y -= 12.2
    y = draw_bullets(c, bullets, y, size)
    if tech:
        y = draw_wrapped(c, tech, LEFT, y - 1.5, RIGHT - LEFT, 8.1, 10.2, MUTED)
    return y - 9


def page_one(c: canvas.Canvas) -> None:
    y = draw_header(c)

    y = draw_section(c, "Summary", y)
    y = draw_wrapped(
        c,
        "Flutter와 Android 기반 앱 개발 경험을 중심으로 WebView 인증, 결제 예외, 실시간 상태, 앱 배포 자동화처럼 "
        "제품 운영에서 자주 깨지는 경계를 정리해 온 모바일 중심 제품 엔지니어입니다. AI 도구는 단순 코드 생성이 아니라 "
        "AGENTS.md, Copilot instructions, 테스트/검증 명령으로 결과를 확인하는 개발 루틴으로 사용합니다.",
        LEFT,
        y,
        RIGHT - LEFT,
        9.0,
        12.3,
    )
    y -= 7

    y = draw_section(c, "Highlights", y)
    y = draw_label_line(c, "Mobile", "Flutter, Android, 앱 생명주기, 스토어 배포, 하이브리드 앱 운영 경험", y)
    y = draw_label_line(c, "Boundary", "WebView, JSBridge, Cookie Auth, Deep Link, PG Payment Flow, SignalR", y)
    y = draw_label_line(c, "AI Workflow", "AGENTS.md, Copilot Instructions, Cursor, AI Coding Guardrail, verification commands", y)
    y -= 6

    y = draw_section(c, "Experience", y)
    y = draw_job(
        c,
        y,
        "실시간 예약 협상 플랫폼 개발 (Dealert)",
        "Flutter 앱 2종과 React 파트너 웹의 결제, 인증, 실시간, 배포 흐름 안정화",
        "2025.07 - 2026.04",
        [
            "PG/WebView/앱 라우팅 경계에서 결제 취소 상태를 성공/실패 흐름과 분리하고 테스트로 고정했습니다.",
            "WebView 쿠키 인증, 자동 로그인 의도, 토큰 갱신 순서를 나눠 로그인 풀림 회귀를 줄였습니다.",
            "Fastlane/Firebase App Distribution 기반 iOS·Android 병렬 배포로 순차 빌드 대비 약 50% 시간을 절약했습니다.",
            "SignalR 기반 실시간 딜/예약 상태 업데이트와 자동 재연결 흐름을 앱과 웹 양쪽에서 정리했습니다.",
            "AGENTS.md, Copilot instructions, React/Flutter 위험 패턴 문서와 검증 명령으로 AI 작업 결과를 확인했습니다.",
        ],
        "Flutter, Dart, React, TypeScript, WebView, SignalR, Fastlane, Firebase, Nginx",
    )

    y = draw_job(
        c,
        y,
        "주식회사 루나소프트 / 그린앤그레이",
        "버티컬 패션 쇼핑몰 셀룩 하이브리드 앱 및 Vue 프론트엔드 개발",
        "2021.05 - 2024.05",
        [
            "Vue 기반 프론트엔드 초기 프로젝트 구조와 빌드 세팅을 구성했습니다.",
            "JSBridge 인터페이스로 Native App과 Web 간의 유기적 통신을 구현했습니다.",
            "React Query, TypeScript, API 문서 기반 코드 생성 흐름을 도입해 반복 구현 비용을 줄였습니다.",
            "배포 시스템과 QA 프로세스를 정리해 릴리즈 안정성을 높였습니다.",
        ],
        "Vue, TypeScript, JSBridge, Hybrid App, React Query",
    )
    draw_job(
        c,
        y,
        "(주)피알앤디컴퍼니 (헤이딜러)",
        "중고차 플랫폼 헤이딜러 고객용/딜러용 Android 앱 개발",
        "2018.10 - 2020.12",
        [
            "딜러 전용 앱 리뉴얼(v3 -> v4)에 참여하고 주요 화면과 사용자 흐름을 구현했습니다.",
            "이미지 첨부 프로세스의 메모리 문제를 Stream 기반 처리로 개선해 앱 안정성과 UX를 높였습니다.",
            "Kotlin 도입과 MVVM 기반 안드로이드 아키텍처 적용을 진행했습니다.",
        ],
        "Android, Kotlin, Java, RxJava, MVVM, Image Pipeline",
        size=8.75,
    )


def page_two(c: canvas.Canvas) -> None:
    y = TOP
    y = draw_section(c, "Earlier Experience", y)
    y = draw_job(
        c,
        y,
        "(주)스펙업애드",
        "보상형 앱 타임스프레드 개발",
        "2018.03 - 2018.09",
        ["상점 화면 등 주요 기능을 개발하고 앱 배포 자동화 프로세스를 구축했습니다."],
        size=8.75,
    )
    y = draw_job(
        c,
        y,
        "(주)씨이랩",
        "리워드 서비스 치즈카운터 개발",
        "2017.02 - 2018.03",
        ["카메라 및 이미지 처리 기능을 개발하고 네트워크 통신 아키텍처를 설계했습니다."],
        size=8.75,
    )
    y = draw_job(
        c,
        y,
        "주식회사 트램스",
        "다수의 Android 앱 외주 및 자체 서비스 개발",
        "2015.07 - 2016.07",
        [
            "식당 매물중개 서비스 앱 초기 설계와 지도 API 연동을 구현했습니다.",
            "통화 화면 커스터마이징, 강연 앱, 물류 PDA 앱 등 다양한 Android 도메인을 개발했습니다.",
        ],
        size=8.75,
    )
    y = draw_job(
        c,
        y,
        "주식회사 애니웨어",
        "Android 앱 개발 실무 참여",
        "2014.03 - 2014.08",
        [],
    )

    y = draw_section(c, "Skills", y - 4)
    y = draw_label_line(c, "Mobile", "Flutter, Dart, Android, Kotlin, Java, RxJava, MVVM, Clean Architecture, Jetpack", y)
    y = draw_label_line(c, "Frontend", "React, Vue, TypeScript, TanStack Query, Zustand", y)
    y = draw_label_line(c, "Release", "Fastlane, Firebase App Distribution, CI/CD, Docker, Nginx Reverse Proxy", y)
    y -= 6

    y = draw_section(c, "Education", y)
    y = draw_label_line(c, "한국방송통신대학교", "컴퓨터과학과 (2019.03 - 2023.02)", y)
    draw_label_line(c, "대전보건대학교", "바이오정보과 (2010.03 - 2014.02)", y)


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
