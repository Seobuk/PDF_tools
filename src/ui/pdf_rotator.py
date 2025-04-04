from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFileDialog, QMessageBox, QSpinBox, QScrollArea, QGridLayout,
    QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
import fitz
import os

class PDFRotatorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.current_pdf_path = None
        self.current_doc = None
        self.current_page = 0
        self.selected_pages = set()  # 선택된 페이지 번호 저장
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
        self.label_info = QLabel("PDF 파일을 선택하고 회전할 페이지를 지정하세요.\n"
                                "Ctrl 키를 누른 상태에서 여러 페이지를 선택할 수 있습니다.")
        self.label_info.setWordWrap(True)
        
        # 파일 선택 영역
        file_layout = QHBoxLayout()
        self.file_path_label = QLabel("선택된 파일: 없음")
        self.file_path_label.setWordWrap(True)
        self.select_file_btn = QPushButton("PDF 선택")
        self.select_file_btn.clicked.connect(self.select_pdf)
        file_layout.addWidget(self.file_path_label)
        file_layout.addWidget(self.select_file_btn)
        
        # 페이지 선택
        page_layout = QGridLayout()
        self.page_spin = QSpinBox()
        self.page_spin.setMinimum(1)
        self.page_spin.valueChanged.connect(self.update_preview)
        page_layout.addWidget(QLabel("페이지:"), 0, 0)
        page_layout.addWidget(self.page_spin, 0, 1)
        
        # 회전 버튼들
        rotate_layout = QHBoxLayout()
        self.rotate_left_btn = QPushButton("90° 왼쪽")
        self.rotate_right_btn = QPushButton("90° 오른쪽")
        self.rotate_left_btn.clicked.connect(lambda: self.rotate_page(-90))
        self.rotate_right_btn.clicked.connect(lambda: self.rotate_page(90))
        rotate_layout.addWidget(self.rotate_left_btn)
        rotate_layout.addWidget(self.rotate_right_btn)
        
        # 저장 버튼
        self.save_btn = QPushButton("변경사항 저장")
        self.save_btn.clicked.connect(self.save_changes)
        
        # 레이아웃에 위젯 추가
        layout.addWidget(self.label_info)
        layout.addLayout(file_layout)
        layout.addLayout(page_layout)
        layout.addLayout(rotate_layout)
        layout.addWidget(self.save_btn)
        layout.addStretch()
        
        return layout

    def setup_right_panel(self):
        layout = QVBoxLayout()
        
        # 미리보기 라벨
        preview_label = QLabel("미리보기")
        preview_label.setAlignment(Qt.AlignCenter)
        
        # 미리보기 스크롤 영역
        self.scroll_area = QScrollArea()
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
        if not self.current_doc:
            return
            
        # 기존 미리보기 제거
        for i in reversed(range(self.preview_layout.count())):
            widget = self.preview_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        # 모든 페이지 미리보기 생성
        for page_num in range(self.current_doc.page_count):
            page = self.current_doc[page_num]
            
            # 페이지 컨테이너 생성
            page_container = QWidget()
            page_layout = QVBoxLayout(page_container)
            
            # 선택 상태에 따른 테두리 스타일 설정
            if page_num in self.selected_pages:
                page_container.setStyleSheet("""
                    QWidget {
                        border: 2px solid #007bff;
                        border-radius: 5px;
                        padding: 5px;
                        background-color: #f8f9fa;
                    }
                """)
            
            # 페이지 번호와 회전 정보 표시
            info_label = QLabel(f"페이지 {page_num + 1} (회전: {page.rotation}°)")
            info_label.setAlignment(Qt.AlignCenter)
            
            # 페이지 렌더링
            pix = page.get_pixmap(matrix=fitz.Matrix(0.3, 0.3))
            
            # PyQt 이미지로 변환
            img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(img)
            
            # 라벨에 이미지 표시
            label = QLabel()
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignCenter)
            
            # 선택 상태 표시
            if page_num in self.selected_pages:
                info_label.setStyleSheet("background-color: #e3f2fd; color: #007bff;")
            
            # 클릭 이벤트 처리
            label.mousePressEvent = lambda e, p=page_num: self.toggle_page_selection(p)
            
            # 컨테이너에 추가
            page_layout.addWidget(info_label)
            page_layout.addWidget(label)
            
            # 메인 레이아웃에 추가
            self.preview_layout.addWidget(page_container)

    def toggle_page_selection(self, page_num):
        if page_num in self.selected_pages:
            self.selected_pages.remove(page_num)
        else:
            self.selected_pages.add(page_num)
        self.update_preview()

    def rotate_page(self, angle):
        if not self.current_doc:
            return
            
        # 선택된 페이지가 없으면 현재 페이지만 회전
        if not self.selected_pages:
            self.selected_pages = {self.page_spin.value() - 1}
        
        # 선택된 모든 페이지 회전
        for page_num in self.selected_pages:
            page = self.current_doc[page_num]
            current_rotation = page.rotation
            new_rotation = (current_rotation + angle) % 360
            page.set_rotation(new_rotation)
        
        # 미리보기 업데이트
        self.update_preview()

    def save_changes(self):
        if not self.current_pdf_path:
            QMessageBox.warning(self, "경고", "PDF 파일을 먼저 선택해주세요.")
            return
            
        # 원본 파일의 경로와 파일명 분리
        original_dir = os.path.dirname(self.current_pdf_path)
        original_filename = os.path.basename(self.current_pdf_path)
        
        # 새 파일명 생성 (원본파일명_rotated.pdf)
        default_name = os.path.splitext(original_filename)[0] + '_rotated.pdf'
        # 전체 경로 생성 (원본경로/원본파일명_rotated.pdf)
        default_save_path = os.path.join(original_dir, default_name)
        
        save_path, _ = QFileDialog.getSaveFileName(
            self, 
            "저장할 위치 선택", 
            default_save_path,  # 원본 파일 경로를 기본 저장 경로로 설정
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