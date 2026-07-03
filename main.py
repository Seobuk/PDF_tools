import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from src.ui.main_window import MainWindow
from src.ui.styles import (
    APP_STYLESHEET, COLOR_BG, COLOR_SURFACE, COLOR_TEXT, COLOR_PRIMARY,
)


def apply_theme(app: QApplication) -> None:
    """밝고 현대적인 라이트 테마를 적용한다."""
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(COLOR_BG))
    palette.setColor(QPalette.WindowText, QColor(COLOR_TEXT))
    palette.setColor(QPalette.Base, QColor(COLOR_SURFACE))
    palette.setColor(QPalette.AlternateBase, QColor(COLOR_BG))
    palette.setColor(QPalette.ToolTipBase, QColor(COLOR_TEXT))
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, QColor(COLOR_TEXT))
    palette.setColor(QPalette.Button, QColor(COLOR_SURFACE))
    palette.setColor(QPalette.ButtonText, QColor(COLOR_TEXT))
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(COLOR_PRIMARY))
    palette.setColor(QPalette.Highlight, QColor(COLOR_PRIMARY))
    palette.setColor(QPalette.HighlightedText, Qt.white)
    palette.setColor(QPalette.Disabled, QPalette.Text, QColor("#a0a7b1"))
    palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor("#a0a7b1"))
    app.setPalette(palette)

    app.setStyleSheet(APP_STYLESHEET)

def main():
    app = QApplication(sys.argv)
    apply_theme(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
