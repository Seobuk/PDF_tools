from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSpinBox, QFileDialog, QMessageBox, QGridLayout
)
from ..utils.pdf_handler import default_output_path
from .preview import clear_layout, add_page_previews, create_zoom_control, create_preview_panel
from .styles import PRIMARY_BUTTON_STYLE, SUCCESS_BUTTON_STYLE, TITLE_LABEL_STYLE
import fitz
import os

class PDFSplitterWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.current_pdf_path = None
        self.current_doc = None
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
        self.label_info = QLabel("PDF 파일을 선택하고 분할할 페이지 범위를 지정하세요.")
        self.label_info.setStyleSheet(TITLE_LABEL_STYLE)

        # 파일 선택 버튼
        self.select_btn = QPushButton("PDF 파일 선택")
        self.select_btn.clicked.connect(self.select_pdf)
        self.select_btn.setStyleSheet(PRIMARY_BUTTON_STYLE)

        # 선택된 파일 경로 표시
        self.file_path_label = QLabel("선택된 파일: 없음")

        # 페이지 범위 설정
        range_layout = QGridLayout()
        self.start_page = QSpinBox()
        self.end_page = QSpinBox()
        self.start_page.setMinimum(1)
        self.end_page.setMinimum(1)
        self.start_page.valueChanged.connect(self.update_preview)
        self.end_page.valueChanged.connect(self.update_preview)
        range_layout.addWidget(QLabel("시작 페이지:"), 0, 0)
        range_layout.addWidget(self.start_page, 0, 1)
        range_layout.addWidget(QLabel("끝 페이지:"), 1, 0)
        range_layout.addWidget(self.end_page, 1, 1)

        # 미리보기 배율
        zoom_layout, self.zoom_spin = create_zoom_control(self.update_preview)

        # 분할 버튼
        self.split_btn = QPushButton("선택한 범위 분할")
        self.split_btn.clicked.connect(self.split_pdf)
        self.split_btn.setEnabled(False)
        self.split_btn.setStyleSheet(SUCCESS_BUTTON_STYLE)

        # 저장 버튼
        self.save_btn = QPushButton("변경사항 저장")
        self.save_btn.clicked.connect(self.save_changes)
        self.save_btn.setStyleSheet(PRIMARY_BUTTON_STYLE)

        # 레이아웃에 위젯 추가
        layout.addWidget(self.label_info)
        layout.addWidget(self.select_btn)
        layout.addWidget(self.file_path_label)
        layout.addLayout(range_layout)
        layout.addLayout(zoom_layout)
        layout.addWidget(self.split_btn)
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

            # 기존 문서가 있으면 닫기
            if self.current_doc:
                self.current_doc.close()

            # 새 문서 열기
            self.current_doc = fitz.open(file_path)
            page_count = self.current_doc.page_count
            self.end_page.setMaximum(page_count)
            self.start_page.setMaximum(page_count)
            self.end_page.setValue(page_count)
            self.split_btn.setEnabled(True)

            # 미리보기 업데이트
            self.update_preview()

    def update_preview(self):
        if not self.current_doc:
            return

        clear_layout(self.preview_layout)
        add_page_previews(
            self.preview_layout,
            self.current_doc,
            self.zoom_spin.value() / 100,
            start=self.start_page.value() - 1,
            end=self.end_page.value(),
        )

    def split_pdf(self):
        self._export_range('_split.pdf', "PDF 분할이 완료되었습니다.")

    def save_changes(self):
        self._export_range('_pages.pdf', "선택한 페이지가 성공적으로 저장되었습니다.")

    def _export_range(self, suffix, success_message):
        """현재 선택된 페이지 범위를 새 PDF로 저장한다."""
        if not self.current_doc:
            QMessageBox.warning(self, "경고", "PDF 파일을 선택해주세요.")
            return

        try:
            start_page = self.start_page.value()
            end_page = self.end_page.value()

            if start_page > end_page:
                QMessageBox.warning(self, "경고", "시작 페이지가 끝 페이지보다 클 수 없습니다.")
                return

            save_path, _ = QFileDialog.getSaveFileName(
                self,
                "저장할 위치 선택",
                default_output_path(self.current_pdf_path, suffix),
                "PDF files (*.pdf)"
            )

            if save_path:
                new_doc = fitz.open()
                new_doc.insert_pdf(
                    self.current_doc,
                    from_page=start_page - 1,
                    to_page=end_page - 1,
                )
                new_doc.save(save_path)
                new_doc.close()

                QMessageBox.information(self, "성공", success_message)
        except Exception as e:
            QMessageBox.critical(self, "오류", f"PDF 저장 중 오류가 발생했습니다: {str(e)}")

    def closeEvent(self, event):
        if self.current_doc:
            self.current_doc.close()
        super().closeEvent(event)
