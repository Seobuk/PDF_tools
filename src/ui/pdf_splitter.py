from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSpinBox, QFileDialog, QMessageBox, QGridLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from ..utils.pdf_handler import PDFHandler
from .zoomable_scroll_area import ZoomableScrollArea
import fitz
import os

class PDFSplitterWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.pdf_handler = PDFHandler()
        self.current_pdf_path = None
        self.current_doc = None
        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout()
        
        # 왼쪽 패널 설정
        left_panel = self.setup_left_panel()
        
        # 오른쪽 패널 설정
        right_panel = self.setup_right_panel()
        
        main_layout.addLayout(left_panel, stretch=1)
        main_layout.addLayout(right_panel, stretch=2)
        self.setLayout(main_layout)

    def setup_left_panel(self):
        layout = QVBoxLayout()
        
        # 설명 라벨
        self.label_info = QLabel("PDF 파일을 선택하고 쪼갤 페이지 범위를 지정하세요.")
        self.label_info.setWordWrap(True)
        
        # 파일 선택 영역
        file_layout = QHBoxLayout()
        self.file_path_label = QLabel("선택된 파일: 없음")
        self.file_path_label.setWordWrap(True)
        self.select_file_btn = QPushButton("PDF 선택")
        self.select_file_btn.clicked.connect(self.select_pdf)
        file_layout.addWidget(self.file_path_label)
        file_layout.addWidget(self.select_file_btn)
        
        # 페이지 범위 지정
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
        zoom_layout = QGridLayout()
        self.zoom_spin = QSpinBox()
        self.zoom_spin.setRange(10, 300)
        self.zoom_spin.setValue(30)
        self.zoom_spin.setSuffix('%')
        self.zoom_spin.valueChanged.connect(self.update_preview)
        zoom_layout.addWidget(QLabel("미리보기 배율:"), 0, 0)
        zoom_layout.addWidget(self.zoom_spin, 0, 1)
        
        # 쪼개기 버튼
        self.split_btn = QPushButton("PDF 쪼개기")
        self.split_btn.clicked.connect(self.split_pdf)
        
        # 저장 버튼
        self.save_btn = QPushButton("선택한 페이지 저장")
        self.save_btn.clicked.connect(self.save_pages)
        
        # 레이아웃에 위젯 추가
        layout.addWidget(self.label_info)
        layout.addLayout(file_layout)
        layout.addLayout(range_layout)
        layout.addLayout(zoom_layout)
        layout.addWidget(self.split_btn)
        layout.addWidget(self.save_btn)
        layout.addStretch()
        
        return layout

    def setup_right_panel(self):
        layout = QVBoxLayout()
        
        # 미리보기 라벨
        preview_label = QLabel("미리보기")
        preview_label.setAlignment(Qt.AlignCenter)
        
        # 미리보기 스크롤 영역
        self.scroll_area = ZoomableScrollArea(self.zoom_spin)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumWidth(400)
        
        # 미리보기 컨테이너
        self.preview_container = QWidget()
        self.preview_layout = QVBoxLayout(self.preview_container)
        self.scroll_area.setWidget(self.preview_container)
        
        layout.addWidget(preview_label)
        layout.addWidget(self.scroll_area)
        
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
            
            # 미리보기 업데이트
            self.update_preview()

    def update_preview(self):
        if not self.current_doc:
            return
            
        # 기존 미리보기 제거
        for i in reversed(range(self.preview_layout.count())):
            widget = self.preview_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        start = self.start_page.value() - 1
        end = self.end_page.value()
        
        # 선택된 페이지 미리보기 생성
        zoom = self.zoom_spin.value() / 100
        for page_num in range(start, end):
            page = self.current_doc[page_num]
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
            
            # PyQt 이미지로 변환
            img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(img)
            
            # 라벨에 이미지 표시
            label = QLabel()
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignCenter)
            
            # 페이지 번호 표시
            page_label = QLabel(f"페이지 {page_num + 1}")
            page_label.setAlignment(Qt.AlignCenter)
            
            # 컨테이너에 추가
            self.preview_layout.addWidget(page_label)
            self.preview_layout.addWidget(label)
            self.preview_layout.addWidget(QLabel(""))  # 간격용

    def split_pdf(self):
        if not self.current_doc:
            QMessageBox.warning(self, "경고", "PDF 파일을 선택해주세요.")
            return
            
        try:
            # 선택된 페이지 범위 가져오기
            start_page = self.start_page.value()
            end_page = self.end_page.value()
            
            if start_page > end_page:
                QMessageBox.warning(self, "경고", "시작 페이지가 끝 페이지보다 클 수 없습니다.")
                return
                
            # 원본 파일의 경로와 파일명 분리
            original_dir = os.path.dirname(self.current_pdf_path)
            original_filename = os.path.basename(self.current_pdf_path)
            
            # 새 파일명 생성 (원본파일명_split.pdf)
            default_name = os.path.splitext(original_filename)[0] + '_split.pdf'
            # 전체 경로 생성 (원본경로/원본파일명_split.pdf)
            default_save_path = os.path.join(original_dir, default_name)
            
            # 저장 경로 선택
            save_path, _ = QFileDialog.getSaveFileName(
                self,
                "저장할 위치 선택",
                default_save_path,  # 원본 파일 경로를 기본 저장 경로로 설정
                "PDF files (*.pdf)"
            )
            
            if save_path:
                # 새 PDF 문서 생성
                new_doc = fitz.open()
                
                # 선택된 페이지 복사
                for page_num in range(start_page - 1, end_page):
                    new_doc.insert_pdf(self.current_doc, from_page=page_num, to_page=page_num)
                
                # 저장
                new_doc.save(save_path)
                new_doc.close()
                
                QMessageBox.information(self, "성공", "PDF 분할이 완료되었습니다.")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"PDF 분할 중 오류가 발생했습니다: {str(e)}")

    def save_pages(self):
        if not self.current_doc:
            QMessageBox.warning(self, "경고", "PDF 파일을 선택해주세요.")
            return
            
        try:
            # 선택된 페이지 범위 가져오기
            start_page = self.start_page.value()
            end_page = self.end_page.value()
            
            if start_page > end_page:
                QMessageBox.warning(self, "경고", "시작 페이지가 끝 페이지보다 클 수 없습니다.")
                return
                
            # 원본 파일의 경로와 파일명 분리
            original_dir = os.path.dirname(self.current_pdf_path)
            original_filename = os.path.basename(self.current_pdf_path)
            
            # 새 파일명 생성 (원본파일명_pages.pdf)
            default_name = os.path.splitext(original_filename)[0] + '_pages.pdf'
            # 전체 경로 생성 (원본경로/원본파일명_pages.pdf)
            default_save_path = os.path.join(original_dir, default_name)
            
            # 저장 경로 선택
            save_path, _ = QFileDialog.getSaveFileName(
                self,
                "저장할 위치 선택",
                default_save_path,  # 원본 파일 경로를 기본 저장 경로로 설정
                "PDF files (*.pdf)"
            )
            
            if save_path:
                # 새 PDF 문서 생성
                new_doc = fitz.open()
                
                # 선택된 페이지 복사
                for page_num in range(start_page - 1, end_page):
                    new_doc.insert_pdf(self.current_doc, from_page=page_num, to_page=page_num)
                
                # 저장
                new_doc.save(save_path)
                new_doc.close()
                
                QMessageBox.information(self, "성공", "선택한 페이지가 성공적으로 저장되었습니다.")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"페이지 저장 중 오류가 발생했습니다: {str(e)}")

    def closeEvent(self, event):
        if self.current_doc:
            self.current_doc.close()
        super().closeEvent(event) 