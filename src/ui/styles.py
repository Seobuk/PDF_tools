"""
공통 스타일 정의
"""

# 버튼 스타일
PRIMARY_BUTTON_STYLE = '''
    QPushButton {
        background-color: #007aff;
        color: white;
        border: none;
        padding: 10px;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #0062cc;
    }
    QPushButton:disabled {
        background-color: #d1d1d6;
    }
'''

SUCCESS_BUTTON_STYLE = '''
    QPushButton {
        background-color: #34c759;
        color: white;
        border: none;
        padding: 10px;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #2fb350;
    }
    QPushButton:disabled {
        background-color: #d1d1d6;
    }
'''

WARNING_BUTTON_STYLE = '''
    QPushButton {
        background-color: #ff9500;
        color: white;
        border: none;
        padding: 10px;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #e68600;
    }
    QPushButton:disabled {
        background-color: #d1d1d6;
    }
'''

DANGER_BUTTON_STYLE = '''
    QPushButton {
        background-color: #ff3b30;
        color: white;
        border: none;
        padding: 10px;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #e62e25;
    }
    QPushButton:disabled {
        background-color: #d1d1d6;
    }
'''

# 라벨 스타일
TITLE_LABEL_STYLE = '''
    QLabel {
        font-size: 14px;
        font-weight: bold;
        color: #000000;
    }
'''

# 진행 상태바 스타일
PROGRESS_BAR_STYLE = '''
    QProgressBar {
        border: none;
        border-radius: 5px;
        background-color: #f2f2f7;
        text-align: center;
    }
    QProgressBar::chunk {
        background-color: #007aff;
        border-radius: 5px;
    }
''' 