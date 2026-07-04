from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QMessageBox, QSpinBox, QGridLayout
)
from PyQt5.QtCore import Qt
from ..utils.pdf_handler import default_output_path
from .preview import clear_layout, render_page_label, create_zoom_control, create_preview_panel
from .styles import (
    PRIMARY_BUTTON_STYLE, SUCCESS_BUTTON_STYLE, TITLE_LABEL_STYLE,
    PAGE_CARD_STYLE, PAGE_CARD_SELECTED_STYLE, PAGE_INFO_SELECTED_STYLE,
)
import fitz
import os

class PDFRotatorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.current_pdf_path = None
        self.current_doc = None
        self.selected_pages = set()  # 선택된 페이지 번호 저장
        self.page_widgets = []  # 페이지별 (컨테이너, 정보 라벨) 캐시
        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout()

        left_panel = self.setup_left_panel()
        right_panel, self.preview_layout = create_preview_panel(self.zoom_spin)

        main_layout.addLayout(left_panel, stretch=1)
        main_layout.addLayout(right_panel, stretch=2)
        self.setLayout(main_layout)

    def setup_left_panel(self):
        layout = QVBoxLayout()

        # 설명 라벨
        self.label_info = QLabel("PDF 파일을 선택하고 회전할 페이지를 선택하세요.")
        self.label_info.setStyleSheet(TITLE_LABEL_STYLE)

        # 파일 선택 버튼
        self.select_btn = QPushButton("PDF 파일 선택")
        self.select_btn.clicked.connect(self.select_pdf)
        self.select_btn.setStyleSheet(PRIMARY_BUTTON_STYLE)

        # 선택된 파일 경로 표시
        self.file_path_label = QLabel("선택된 파일: 없음")

        # 페이지 선택
        page_layout = QGridLayout()
        self.page_spin = QSpinBox()
        self.page_spin.setMinimum(1)
        page_layout.addWidget(QLabel("페이지:"), 0, 0)
        page_layout.addWidget(self.page_spin, 0, 1)

        # 미리보기 배율
        zoom_layout, self.zoom_spin = create_zoom_control(self.update_preview)

        # 회전 버튼
        rotate_layout = QHBoxLayout()
        self.rotate_left_btn = QPushButton("90° 왼쪽")
        self.rotate_right_btn = QPushButton("90° 오른쪽")
        self.rotate_left_btn.clicked.connect(lambda: self.rotate_page(-90))
        self.rotate_right_btn.clicked.connect(lambda: self.rotate_page(90))
        self.rotate_left_btn.setStyleSheet(PRIMARY_BUTTON_STYLE)
        self.rotate_right_btn.setStyleSheet(PRIMARY_BUTTON_STYLE)
        rotate_layout.addWidget(self.rotate_left_btn)
        rotate_layout.addWidget(self.rotate_right_btn)

        # 저장 버튼
        self.save_btn = QPushButton("변경사항 저장")
        self.save_btn.clicked.connect(self.save_changes)
        self.save_btn.setStyleSheet(SUCCESS_BUTTON_STYLE)

        # 레이아웃에 위젯 추가
        layout.addWidget(self.label_info)
        layout.addWidget(self.select_btn)
        layout.addWidget(self.file_path_label)
        layout.addLayout(page_layout)
        layout.addLayout(zoom_layout)
        layout.addLayout(rotate_layout)
        layout.addWidget(self.save_btn)
        layout.addStretch()

        return layout

    def select_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "PDF 파일 선택",
            "",
            "PDF files (*.pdf)"
        )
        if file_path:
            self.current_pdf_path = file_path
            self.file_path_label.setText(f"선택된 파일: {os.path.basename(file_path)}")
            self.selected_pages.clear()  # 선택된 페이지 초기화

            # 기존 문서가 있으면 닫기
            if self.current_doc:
                self.current_doc.close()

            # 새 문서 열기
            self.current_doc = fitz.open(file_path)
            self.page_spin.setMaximum(self.current_doc.page_count)
            self.page_spin.setValue(1)

            # 미리보기 업데이트
            self.update_preview()

    def update_preview(self):
        """모든 페이지 미리보기를 새로 만든다 (파일 선택/배율 변경 시)."""
        if not self.current_doc:
            return

        clear_layout(self.preview_layout)
        self.page_widgets = []

        for page_num in range(self.current_doc.page_count):
            page_container = QWidget()
            page_layout = QVBoxLayout(page_container)

            info_label = QLabel()
            info_label.setAlignment(Qt.AlignCenter)

            image_label = self._render_page(page_num)

            page_layout.addWidget(info_label)
            page_layout.addWidget(image_label)
            self.preview_layout.addWidget(page_container)

            self.page_widgets.append((page_container, info_label))
            self._apply_page_state(page_num)

    def _render_page(self, page_num):
        label = render_page_label(self.current_doc[page_num], self.zoom_spin.value() / 100)
        label.mousePressEvent = lambda e, p=page_num: self.toggle_page_selection(p)
        return label

    def _apply_page_state(self, page_num):
        """선택 여부와 회전 정보를 해당 페이지 위젯에만 반영한다."""
        container, info_label = self.page_widgets[page_num]
        selected = page_num in self.selected_pages
        rotation = self.current_doc[page_num].rotation

        container.setStyleSheet(PAGE_CARD_SELECTED_STYLE if selected else PAGE_CARD_STYLE)
        info_label.setStyleSheet(PAGE_INFO_SELECTED_STYLE if selected else "")
        info_label.setText(f"페이지 {page_num + 1} (회전: {rotation}°)")

    def _refresh_page_image(self, page_num):
        """회전 후 해당 페이지의 이미지만 다시 렌더링한다."""
        container, _ = self.page_widgets[page_num]
        layout = container.layout()
        old_label = layout.itemAt(1).widget()
        layout.replaceWidget(old_label, self._render_page(page_num))
        old_label.deleteLater()

    def toggle_page_selection(self, page_num):
        if page_num in self.selected_pages:
            self.selected_pages.remove(page_num)
        else:
            self.selected_pages.add(page_num)
        self._apply_page_state(page_num)

    def rotate_page(self, angle):
        if not self.current_doc:
            return

        # 선택된 페이지가 없으면 현재 페이지만 회전
        if not self.selected_pages:
            self.selected_pages = {self.page_spin.value() - 1}

        # 선택된 페이지만 회전하고 해당 미리보기만 갱신
        for page_num in self.selected_pages:
            page = self.current_doc[page_num]
            page.set_rotation((page.rotation + angle) % 360)
            self._refresh_page_image(page_num)
            self._apply_page_state(page_num)

    def save_changes(self):
        if not self.current_pdf_path:
            QMessageBox.warning(self, "경고", "PDF 파일을 먼저 선택해주세요.")
            return

        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "저장할 위치 선택",
            default_output_path(self.current_pdf_path, '_rotated.pdf'),
            "PDF files (*.pdf)"
        )

        if save_path:
            try:
                self.current_doc.save(save_path)
                QMessageBox.information(self, "성공", "변경사항이 저장되었습니다.")
            except Exception as e:
                QMessageBox.critical(self, "오류", f"저장 중 오류가 발생했습니다: {str(e)}")

    def closeEvent(self, event):
        if self.current_doc:
            self.current_doc.close()
        super().closeEvent(event)
