from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QMessageBox, QSpinBox, QGridLayout,
    QComboBox
)
from .preview import clear_layout, add_page_previews, create_zoom_control, create_preview_panel
from .styles import PRIMARY_BUTTON_STYLE, SUCCESS_BUTTON_STYLE, TITLE_LABEL_STYLE
import fitz
import os

class PDFToImageWidget(QWidget):
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
        self.label_info = QLabel("PDF 파일을 선택하고 이미지로 변환할 페이지 범위를 지정하세요.")
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
        range_layout.addWidget(QLabel("시작 페이지:"), 0, 0)
        range_layout.addWidget(self.start_page, 0, 1)
        range_layout.addWidget(QLabel("끝 페이지:"), 1, 0)
        range_layout.addWidget(self.end_page, 1, 1)

        # 이미지 형식 선택
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("이미지 형식:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["PNG", "JPEG"])
        format_layout.addWidget(self.format_combo)

        # 미리보기 배율
        zoom_layout, self.zoom_spin = create_zoom_control(self.update_preview)

        # 변환 버튼
        self.convert_btn = QPushButton("이미지로 변환")
        self.convert_btn.clicked.connect(self.convert_to_images)
        self.convert_btn.setEnabled(False)
        self.convert_btn.setStyleSheet(SUCCESS_BUTTON_STYLE)

        # 레이아웃에 위젯 추가
        layout.addWidget(self.label_info)
        layout.addSpacing(8)
        layout.addWidget(self.select_btn)
        layout.addSpacing(4)
        layout.addWidget(self.file_path_label)
        layout.addSpacing(8)
        layout.addLayout(range_layout)
        layout.addSpacing(4)
        layout.addLayout(format_layout)
        layout.addSpacing(4)
        layout.addLayout(zoom_layout)
        layout.addSpacing(12)
        layout.addWidget(self.convert_btn)
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

            # 변환 버튼 활성화
            self.convert_btn.setEnabled(True)

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

    def convert_to_images(self):
        if not self.current_pdf_path:
            QMessageBox.warning(self, "경고", "PDF 파일을 선택해주세요.")
            return

        try:
            # 저장할 디렉토리 선택
            save_dir = QFileDialog.getExistingDirectory(
                self,
                "이미지 저장할 폴더 선택",
                os.path.dirname(self.current_pdf_path)
            )

            if save_dir:
                format_type = self.format_combo.currentText().lower()
                dpi = 300  # 기본 DPI
                matrix = fitz.Matrix(dpi / 72.0, dpi / 72.0)

                start_page = self.start_page.value()
                end_page = self.end_page.value()

                for page_num in range(start_page - 1, end_page):
                    pix = self.current_doc[page_num].get_pixmap(matrix=matrix)
                    image_path = os.path.join(save_dir, f"page_{page_num + 1}.{format_type}")

                    if format_type == "jpeg":
                        pix.save(image_path, "jpeg", jpg_quality=100)
                    else:  # png
                        pix.save(image_path, "png")

                QMessageBox.information(
                    self,
                    "성공",
                    f"이미지 변환이 완료되었습니다.\n저장 위치: {save_dir}"
                )
        except Exception as e:
            QMessageBox.critical(self, "오류", f"이미지 변환 중 오류가 발생했습니다: {str(e)}")

    def closeEvent(self, event):
        if self.current_doc:
            self.current_doc.close()
        super().closeEvent(event)
