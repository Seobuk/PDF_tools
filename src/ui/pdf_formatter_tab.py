from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QGridLayout, QProgressBar
)
from .preview import clear_layout, add_page_previews, create_zoom_control, create_preview_panel
from .styles import PRIMARY_BUTTON_STYLE, SUCCESS_BUTTON_STYLE, PROGRESS_BAR_STYLE
from ..utils.pdf_handler import default_output_path
import fitz
import os
from PyPDF2 import PdfReader, PdfWriter

# A4 크기 (포인트 단위)
A4_WIDTH = 595
A4_HEIGHT = 842

class PdfFormatterTab(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_file = None
        self.current_doc = None
        self.converted_doc = None
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

        # PDF 선택 버튼
        self.select_button = QPushButton('PDF 파일 선택')
        self.select_button.clicked.connect(self.selectFile)
        self.select_button.setStyleSheet(PRIMARY_BUTTON_STYLE)

        # 선택된 파일 경로 표시
        self.fileLabel = QLabel('선택된 파일: 없음')
        self.fileLabel.setWordWrap(True)

        # 미리보기 배율
        zoom_layout, self.zoom_spin = create_zoom_control(self.update_preview)

        # 변환 버튼
        self.convertButton = QPushButton('A4 형식으로 변환')
        self.convertButton.clicked.connect(self.convertToA4)
        self.convertButton.setEnabled(False)
        self.convertButton.setStyleSheet(SUCCESS_BUTTON_STYLE)

        # 진행 상태바
        self.progressBar = QProgressBar()
        self.progressBar.setVisible(False)
        self.progressBar.setStyleSheet(PROGRESS_BAR_STYLE)

        layout.addWidget(self.select_button)
        layout.addWidget(self.fileLabel)
        layout.addLayout(zoom_layout)
        layout.addWidget(self.convertButton)
        layout.addWidget(self.progressBar)
        layout.addStretch()

        return layout

    def selectFile(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'PDF 파일 선택', '',
                                             'PDF 파일 (*.pdf)')
        if fname:
            self.selected_file = fname
            self.fileLabel.setText(f'선택된 파일: {os.path.basename(fname)}')
            self.convertButton.setEnabled(True)

            # 기존 문서가 있으면 닫기
            if self.current_doc:
                self.current_doc.close()

            self.current_doc = fitz.open(fname)
            self.converted_doc = None
            self.update_preview()

    def convertToA4(self):
        if not self.selected_file:
            return

        save_path, _ = QFileDialog.getSaveFileName(
            self,
            '저장할 위치 선택',
            default_output_path(self.selected_file, '_a4.pdf'),
            'PDF 파일 (*.pdf)'
        )

        if not save_path:
            return

        try:
            self.progressBar.setVisible(True)
            reader = PdfReader(self.selected_file)
            writer = PdfWriter()

            self.progressBar.setMaximum(len(reader.pages))

            for i, page in enumerate(reader.pages):
                # 원본 페이지 크기 가져오기
                original_width = float(page.mediabox.width)
                original_height = float(page.mediabox.height)

                # 축소 비율 계산 (확대는 하지 않음)
                scale = min(A4_WIDTH / original_width, A4_HEIGHT / original_height, 1.0)

                # 왼쪽 위 정렬: 아래쪽 여백만큼 위로 이동
                y_pos = A4_HEIGHT - original_height * scale

                page.add_transformation([scale, 0, 0, scale, 0, y_pos])
                page.mediabox.upper_right = (A4_WIDTH, A4_HEIGHT)
                writer.add_page(page)
                self.progressBar.setValue(i + 1)

            with open(save_path, 'wb') as output_file:
                writer.write(output_file)

            self.fileLabel.setText(f'변환 완료! 저장 위치: {save_path}')

            if self.converted_doc:
                self.converted_doc.close()
            self.converted_doc = fitz.open(save_path)
            self.update_preview()

        except Exception as e:
            self.fileLabel.setText(f'오류 발생: {str(e)}')
        finally:
            self.progressBar.setVisible(False)

    def update_preview(self):
        if not self.current_doc:
            return

        clear_layout(self.preview_layout)
        zoom = self.zoom_spin.value() / 100

        self.preview_layout.addWidget(QLabel('변환 전'))
        add_page_previews(self.preview_layout, self.current_doc, zoom)

        if self.converted_doc:
            self.preview_layout.addWidget(QLabel('변환 후'))
            add_page_previews(self.preview_layout, self.converted_doc, zoom)

    def closeEvent(self, event):
        if self.current_doc:
            self.current_doc.close()
        if self.converted_doc:
            self.converted_doc.close()
        super().closeEvent(event)
