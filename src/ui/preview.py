"""
미리보기 관련 공통 헬퍼

각 탭에서 반복되던 미리보기 패널 구성, 페이지 렌더링, 레이아웃 비우기
로직을 한곳에 모은다.
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QSpinBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
import fitz

from .zoomable_scroll_area import ZoomableScrollArea
from .styles import TITLE_LABEL_STYLE


def clear_layout(layout):
    """레이아웃 안의 모든 항목을 제거한다."""
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget:
            widget.deleteLater()


def render_page_label(page, zoom):
    """PDF 페이지를 렌더링한 QLabel을 반환한다."""
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
    img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
    label = QLabel()
    label.setPixmap(QPixmap.fromImage(img))
    label.setAlignment(Qt.AlignCenter)
    return label


def add_page_previews(layout, doc, zoom, start=0, end=None):
    """문서의 [start, end) 페이지를 '페이지 N' 라벨과 함께 레이아웃에 추가한다."""
    if end is None:
        end = doc.page_count
    for page_num in range(start, end):
        page_label = QLabel(f"페이지 {page_num + 1}")
        page_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(page_label)
        layout.addWidget(render_page_label(doc[page_num], zoom))
        layout.addSpacing(12)


def create_zoom_control(on_change, initial=30):
    """미리보기 배율 스핀박스와 라벨 레이아웃을 만들어 (layout, spinbox)로 반환한다."""
    zoom_spin = QSpinBox()
    zoom_spin.setRange(10, 300)
    zoom_spin.setValue(initial)
    zoom_spin.setSuffix('%')
    zoom_spin.valueChanged.connect(on_change)

    layout = QGridLayout()
    layout.addWidget(QLabel('미리보기 배율:'), 0, 0)
    layout.addWidget(zoom_spin, 0, 1)
    return layout, zoom_spin


def create_preview_panel(zoom_spin, title='미리보기'):
    """제목 + 확대 가능한 스크롤 미리보기 패널을 만든다.

    Returns
    -------
    (QVBoxLayout, QVBoxLayout)
        (탭에 붙일 패널 레이아웃, 페이지 위젯을 추가할 미리보기 레이아웃)
    """
    panel = QVBoxLayout()

    title_label = QLabel(title)
    title_label.setAlignment(Qt.AlignCenter)
    title_label.setStyleSheet(TITLE_LABEL_STYLE)

    scroll_area = ZoomableScrollArea(zoom_spin)
    scroll_area.setWidgetResizable(True)
    scroll_area.setMinimumWidth(400)

    container = QWidget()
    preview_layout = QVBoxLayout(container)
    scroll_area.setWidget(container)

    panel.addWidget(title_label)
    panel.addWidget(scroll_area)
    return panel, preview_layout
