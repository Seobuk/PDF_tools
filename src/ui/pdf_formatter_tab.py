from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QMessageBox, QSpinBox, QGridLayout,
    QProgressBar
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from .zoomable_scroll_area import ZoomableScrollArea
from .styles import PRIMARY_BUTTON_STYLE, SUCCESS_BUTTON_STYLE, PROGRESS_BAR_STYLE, TITLE_LABEL_STYLE
import fitz
import os
from PyPDF2 import PdfReader, PdfWriter

class PdfFormatterTab(QWidget):
    def __init__(self):
        super().__init__()
        self.current_doc = None
        self.converted_doc = None
        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout()

        left_panel = self.setup_left_panel()
        right_panel = self.setup_right_panel()

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
        zoom_layout = QGridLayout()
        self.zoom_spin = QSpinBox()
        self.zoom_spin.setRange(10, 300)
        self.zoom_spin.setValue(30)
        self.zoom_spin.setSuffix('%')
        self.zoom_spin.valueChanged.connect(self.update_preview)
        zoom_layout.addWidget(QLabel('미리보기 배율:'), 0, 0)
        zoom_layout.addWidget(self.zoom_spin, 0, 1)

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

    def setup_right_panel(self):
        layout = QVBoxLayout()

        preview_label = QLabel('미리보기')
        preview_label.setAlignment(Qt.AlignCenter)
        preview_label.setStyleSheet(TITLE_LABEL_STYLE)

        self.scroll_area = ZoomableScrollArea(self.zoom_spin)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumWidth(400)

        self.preview_container = QWidget()
        self.preview_layout = QVBoxLayout(self.preview_container)
        self.scroll_area.setWidget(self.preview_container)

        layout.addWidget(preview_label)
        layout.addWidget(self.scroll_area)

        return layout

    def handleDroppedFile(self, file_path):
        if file_path.lower().endswith('.pdf'):
            self.selected_file = file_path
            self.fileLabel.setText(f'선택된 파일: {os.path.basename(file_path)}')
            self.convertButton.setEnabled(True)
            self.dropArea.setText('PDF 파일이 선택되었습니다\n다른 파일을 드래그하여 변경할 수 있습니다')

            # 기존 문서가 있으면 닫기
            if self.current_doc:
                self.current_doc.close()

            self.current_doc = fitz.open(file_path)
            self.converted_doc = None
            self.update_preview()

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
        if hasattr(self, 'selected_file'):
            # 원본 파일의 경로와 파일명 분리
            original_dir = os.path.dirname(self.selected_file)
            original_filename = os.path.basename(self.selected_file)
            
            # 새 파일명 생성 (원본파일명_a4.pdf)
            default_name = os.path.splitext(original_filename)[0] + '_a4.pdf'
            # 전체 경로 생성 (원본경로/원본파일명_a4.pdf)
            default_save_path = os.path.join(original_dir, default_name)
            
            save_path, _ = QFileDialog.getSaveFileName(
                self,
                '저장할 위치 선택',
                default_save_path,  # 원본 파일 경로를 기본 저장 경로로 설정
                'PDF 파일 (*.pdf)'
            )
            
            if not save_path:
                return
                
            try:
                self.progressBar.setVisible(True)
                reader = PdfReader(self.selected_file)
                writer = PdfWriter()
                
                self.progressBar.setMaximum(len(reader.pages))
                
                # A4 크기 설정 (595 x 842 포인트)
                a4_width = 595
                a4_height = 842
                
                for i, page in enumerate(reader.pages):
                    # 원본 페이지 크기 가져오기
                    original_width = float(page.mediabox.width)
                    original_height = float(page.mediabox.height)
                    
                    # 축소 비율 계산
                    width_ratio = a4_width / original_width
                    height_ratio = a4_height / original_height
                    scale = min(width_ratio, height_ratio, 1.0)
                    
                    # 변환된 크기 계산
                    new_width = original_width * scale
                    new_height = original_height * scale
                    
                    # 왼쪽 위 정렬을 위한 위치 계산
                    x_pos = 0
                    y_pos = a4_height - new_height
                    
                    # 변환 행렬 생성
                    page.add_transformation([
                        scale, 0,
                        0, scale,
                        x_pos,
                        y_pos
                    ])
                    
                    page.mediabox.upper_right = (a4_width, a4_height)
                    writer.add_page(page)
                    self.progressBar.setValue(i + 1)
                
                with open(save_path, 'wb') as output_file:
                    writer.write(output_file)

                self.fileLabel.setText(f'변환 완료! 저장 위치: {save_path}')
                self.dropArea.setText('여기에 PDF 파일을 드래그하세요\n또는 클릭하여 파일을 선택하세요')

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

        for i in reversed(range(self.preview_layout.count())):
            widget = self.preview_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        zoom = self.zoom_spin.value() / 100

        self.preview_layout.addWidget(QLabel('변환 전'))
        for page_num in range(self.current_doc.page_count):
            page = self.current_doc[page_num]
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
            img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(img)
            label = QLabel()
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignCenter)
            page_label = QLabel(f'페이지 {page_num + 1}')
            page_label.setAlignment(Qt.AlignCenter)
            self.preview_layout.addWidget(page_label)
            self.preview_layout.addWidget(label)
            self.preview_layout.addWidget(QLabel(''))

        if self.converted_doc:
            self.preview_layout.addWidget(QLabel('변환 후'))
            for page_num in range(self.converted_doc.page_count):
                page = self.converted_doc[page_num]
                pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
                img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(img)
                label = QLabel()
                label.setPixmap(pixmap)
                label.setAlignment(Qt.AlignCenter)
                page_label = QLabel(f'페이지 {page_num + 1}')
                page_label.setAlignment(Qt.AlignCenter)
                self.preview_layout.addWidget(page_label)
                self.preview_layout.addWidget(label)
                self.preview_layout.addWidget(QLabel(''))

    def closeEvent(self, event):
        if self.current_doc:
            self.current_doc.close()
        if self.converted_doc:
            self.converted_doc.close()
        super().closeEvent(event)
