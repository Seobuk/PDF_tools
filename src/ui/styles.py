"""
공통 스타일 정의

v1.1 시절의 기본(Fusion) 디자인을 유지한다. 위젯들이 공통으로 import하는
상수는 남겨두되, 빈 문자열이면 Qt 기본 모양 그대로 렌더링된다.
"""

# 버튼 스타일 (기본 모양 사용)
PRIMARY_BUTTON_STYLE = ""
SUCCESS_BUTTON_STYLE = ""
WARNING_BUTTON_STYLE = ""
DANGER_BUTTON_STYLE = ""

# 라벨 스타일 (기본 모양 사용)
TITLE_LABEL_STYLE = ""
MUTED_LABEL_STYLE = ""

# 진행 상태바 스타일 (기본 모양 사용)
PROGRESS_BAR_STYLE = ""

# PDF 회전 탭: 페이지 선택 표시 (v1.1과 동일)
PAGE_CARD_STYLE = ""
PAGE_CARD_SELECTED_STYLE = '''
    QWidget {
        border: 2px solid #007bff;
        border-radius: 5px;
        padding: 5px;
        background-color: #f8f9fa;
    }
'''
PAGE_INFO_SELECTED_STYLE = "background-color: #e3f2fd; color: #007bff;"
