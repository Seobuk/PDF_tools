"""
공통 디자인 시스템 정의

시맨틱 컬러 토큰과 전역 스타일시트(APP_STYLESHEET), 컴포넌트별 스타일을 제공한다.
- 본문 텍스트 대비 4.5:1 이상, 보조 텍스트 3:1 이상 유지
- hover / pressed / disabled / focus 상태를 시각적으로 구분
- 4/8px 스페이싱 리듬, 8px 코너 반경
"""

# ---------------------------------------------------------------------------
# 컬러 토큰
# ---------------------------------------------------------------------------
COLOR_BG = "#f6f7f9"            # 앱 배경
COLOR_SURFACE = "#ffffff"       # 카드/패널 배경
COLOR_BORDER = "#e2e5ea"        # 기본 테두리
COLOR_BORDER_STRONG = "#c9cfd8" # 입력 위젯 테두리
COLOR_TEXT = "#1b1f27"          # 기본 텍스트 (흰 배경 대비 15.8:1)
COLOR_TEXT_MUTED = "#5a6472"    # 보조 텍스트 (흰 배경 대비 5.9:1)

COLOR_PRIMARY = "#2563eb"
COLOR_PRIMARY_HOVER = "#1d4ed8"
COLOR_PRIMARY_PRESSED = "#1e40af"
COLOR_PRIMARY_TINT = "#eff4fe"

COLOR_SUCCESS = "#15803d"
COLOR_SUCCESS_HOVER = "#166534"
COLOR_SUCCESS_PRESSED = "#14532d"

COLOR_WARNING = "#b45309"
COLOR_WARNING_HOVER = "#92400e"
COLOR_WARNING_PRESSED = "#78350f"

COLOR_DANGER = "#dc2626"
COLOR_DANGER_HOVER = "#b91c1c"
COLOR_DANGER_PRESSED = "#991b1b"

COLOR_DISABLED_BG = "#e8eaee"
COLOR_DISABLED_TEXT = "#a0a7b1"
COLOR_FOCUS = "#93b4f8"


def _solid_button(base: str, hover: str, pressed: str) -> str:
    """단색 배경 버튼 스타일을 생성한다."""
    return f'''
    QPushButton {{
        background-color: {base};
        color: #ffffff;
        border: 1px solid {base};
        padding: 9px 16px;
        border-radius: 8px;
        font-weight: 600;
    }}
    QPushButton:hover {{
        background-color: {hover};
        border-color: {hover};
    }}
    QPushButton:pressed {{
        background-color: {pressed};
        border-color: {pressed};
    }}
    QPushButton:focus {{
        border: 1px solid {COLOR_FOCUS};
    }}
    QPushButton:disabled {{
        background-color: {COLOR_DISABLED_BG};
        border-color: {COLOR_DISABLED_BG};
        color: {COLOR_DISABLED_TEXT};
    }}
'''


# 버튼 스타일
PRIMARY_BUTTON_STYLE = _solid_button(COLOR_PRIMARY, COLOR_PRIMARY_HOVER, COLOR_PRIMARY_PRESSED)
SUCCESS_BUTTON_STYLE = _solid_button(COLOR_SUCCESS, COLOR_SUCCESS_HOVER, COLOR_SUCCESS_PRESSED)
WARNING_BUTTON_STYLE = _solid_button(COLOR_WARNING, COLOR_WARNING_HOVER, COLOR_WARNING_PRESSED)
DANGER_BUTTON_STYLE = _solid_button(COLOR_DANGER, COLOR_DANGER_HOVER, COLOR_DANGER_PRESSED)

# 라벨 스타일
TITLE_LABEL_STYLE = f'''
    QLabel {{
        font-size: 14px;
        font-weight: 700;
        color: {COLOR_TEXT};
        padding: 2px 0 6px 0;
    }}
'''

MUTED_LABEL_STYLE = f'''
    QLabel {{
        color: {COLOR_TEXT_MUTED};
    }}
'''

# 진행 상태바 스타일
PROGRESS_BAR_STYLE = f'''
    QProgressBar {{
        border: none;
        border-radius: 6px;
        background-color: {COLOR_DISABLED_BG};
        text-align: center;
        color: {COLOR_TEXT};
        min-height: 12px;
    }}
    QProgressBar::chunk {{
        background-color: {COLOR_PRIMARY};
        border-radius: 6px;
    }}
'''

# 미리보기 페이지 카드 스타일 (PDF 회전 탭)
PAGE_CARD_STYLE = f'''
    QWidget {{
        border: 1px solid {COLOR_BORDER};
        border-radius: 8px;
        background-color: {COLOR_SURFACE};
    }}
    QLabel {{
        border: none;
        background: transparent;
    }}
'''

PAGE_CARD_SELECTED_STYLE = f'''
    QWidget {{
        border: 2px solid {COLOR_PRIMARY};
        border-radius: 8px;
        background-color: {COLOR_PRIMARY_TINT};
    }}
    QLabel {{
        border: none;
        background: transparent;
    }}
'''

PAGE_INFO_SELECTED_STYLE = f"color: {COLOR_PRIMARY_HOVER}; font-weight: 600;"

# ---------------------------------------------------------------------------
# 전역 스타일시트
# ---------------------------------------------------------------------------
APP_STYLESHEET = f'''
    QWidget {{
        font-family: "Segoe UI", "Malgun Gothic", "Apple SD Gothic Neo", sans-serif;
        font-size: 13px;
        color: {COLOR_TEXT};
    }}

    QMainWindow, QDialog, QMessageBox {{
        background-color: {COLOR_BG};
    }}

    /* 탭 */
    QTabWidget::pane {{
        border: 1px solid {COLOR_BORDER};
        border-radius: 10px;
        background-color: {COLOR_SURFACE};
        top: 6px;
    }}
    QTabBar::tab {{
        background: transparent;
        color: {COLOR_TEXT_MUTED};
        padding: 8px 14px;
        margin: 0 4px 6px 0;
        border-radius: 8px;
        font-weight: 600;
    }}
    QTabBar::tab:hover {{
        background-color: #eceef2;
        color: {COLOR_TEXT};
    }}
    QTabBar::tab:selected {{
        background-color: {COLOR_PRIMARY};
        color: #ffffff;
    }}

    /* 기본(보조) 버튼 */
    QPushButton {{
        background-color: {COLOR_SURFACE};
        color: {COLOR_TEXT};
        border: 1px solid {COLOR_BORDER_STRONG};
        padding: 8px 14px;
        border-radius: 8px;
    }}
    QPushButton:hover {{
        background-color: #f2f4f7;
    }}
    QPushButton:pressed {{
        background-color: {COLOR_DISABLED_BG};
    }}
    QPushButton:focus {{
        border: 1px solid {COLOR_PRIMARY};
    }}
    QPushButton:disabled {{
        background-color: {COLOR_DISABLED_BG};
        border-color: {COLOR_DISABLED_BG};
        color: {COLOR_DISABLED_TEXT};
    }}

    /* 목록 */
    QListWidget {{
        background-color: {COLOR_SURFACE};
        border: 1px solid {COLOR_BORDER};
        border-radius: 8px;
        padding: 4px;
    }}
    QListWidget::item {{
        padding: 8px 10px;
        border-radius: 6px;
        color: {COLOR_TEXT};
    }}
    QListWidget::item:hover {{
        background-color: #f2f4f7;
    }}
    QListWidget::item:selected {{
        background-color: {COLOR_PRIMARY_TINT};
        color: {COLOR_PRIMARY_HOVER};
    }}

    /* 입력 위젯 */
    QSpinBox, QComboBox, QLineEdit {{
        background-color: {COLOR_SURFACE};
        border: 1px solid {COLOR_BORDER_STRONG};
        border-radius: 8px;
        padding: 6px 10px;
        min-height: 18px;
        selection-background-color: {COLOR_PRIMARY};
        selection-color: #ffffff;
    }}
    QSpinBox:hover, QComboBox:hover, QLineEdit:hover {{
        border-color: #a9b1bc;
    }}
    QSpinBox:focus, QComboBox:focus, QLineEdit:focus {{
        border-color: {COLOR_PRIMARY};
    }}
    QComboBox::drop-down {{
        border: none;
        width: 24px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {COLOR_SURFACE};
        border: 1px solid {COLOR_BORDER};
        border-radius: 8px;
        selection-background-color: {COLOR_PRIMARY_TINT};
        selection-color: {COLOR_PRIMARY_HOVER};
        outline: none;
    }}

    /* 체크박스 */
    QCheckBox {{
        spacing: 8px;
    }}
    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
        border: 1px solid {COLOR_BORDER_STRONG};
        border-radius: 5px;
        background-color: {COLOR_SURFACE};
    }}
    QCheckBox::indicator:hover {{
        border-color: {COLOR_PRIMARY};
    }}
    QCheckBox::indicator:checked {{
        background-color: {COLOR_PRIMARY};
        border-color: {COLOR_PRIMARY};
    }}

    /* 스크롤 영역 */
    QScrollArea {{
        border: 1px solid {COLOR_BORDER};
        border-radius: 10px;
        background-color: {COLOR_SURFACE};
    }}
    QScrollArea > QWidget > QWidget {{
        background-color: {COLOR_SURFACE};
    }}

    /* 스크롤바 */
    QScrollBar:vertical {{
        background: transparent;
        width: 10px;
        margin: 2px;
    }}
    QScrollBar::handle:vertical {{
        background: #c4cad3;
        border-radius: 4px;
        min-height: 32px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: #a9b1bc;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0;
    }}
    QScrollBar:horizontal {{
        background: transparent;
        height: 10px;
        margin: 2px;
    }}
    QScrollBar::handle:horizontal {{
        background: #c4cad3;
        border-radius: 4px;
        min-width: 32px;
    }}
    QScrollBar::handle:horizontal:hover {{
        background: #a9b1bc;
    }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0;
    }}
    QScrollBar::add-page, QScrollBar::sub-page {{
        background: transparent;
    }}

    /* 툴팁 */
    QToolTip {{
        background-color: {COLOR_TEXT};
        color: #ffffff;
        border: none;
        padding: 6px 8px;
    }}
'''
