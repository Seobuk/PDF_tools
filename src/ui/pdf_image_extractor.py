from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QMessageBox, QSpinBox, QGridLayout,
    QListWidget, QListWidgetItem, QCheckBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from .zoomable_scroll_area import ZoomableScrollArea
import fitz
import os
from PIL import Image
import io

class PDFImageExtractorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.current_pdf_path = None
        self.current_doc = None
        self.images = []  # 추출된 이미지 정보 저장
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
        self.label_info = QLabel("PDF 문서에서 이미지를 추출하여 저장할 수 있습니다.\n"
                                "이미지를 선택하고 저장할 폴더를 지정하세요.")
        self.label_info.setWordWrap(True)
        
        # 파일 선택 영역
        file_layout = QHBoxLayout()
        self.file_path_label = QLabel("선택된 문서: 없음")
        self.file_path_label.setWordWrap(True)
        self.select_file_btn = QPushButton("PDF 문서 선택")
        self.select_file_btn.clicked.connect(self.select_pdf)
        file_layout.addWidget(self.file_path_label)
        file_layout.addWidget(self.select_file_btn)

        
        
        # 전체 선택 체크박스
        self.select_all_checkbox = QCheckBox("모든 이미지 선택")
        self.select_all_checkbox.stateChanged.connect(self.toggle_select_all)
        
        # 이미지 목록
        self.image_list = QListWidget()
        self.image_list.setSelectionMode(QListWidget.MultiSelection)
        self.image_list.itemClicked.connect(self.show_image)
        self.image_list.currentItemChanged.connect(self.show_image)

        # 미리보기 배율
        zoom_layout = QGridLayout()
        self.zoom_spin = QSpinBox()
        self.zoom_spin.setRange(10, 300)
        self.zoom_spin.setValue(100)
        self.zoom_spin.setSuffix('%')
        self.zoom_spin.valueChanged.connect(lambda: self.show_image(self.image_list.currentItem()))
        zoom_layout.addWidget(QLabel("미리보기 배율:"), 0, 0)
        zoom_layout.addWidget(self.zoom_spin, 0, 1)

        # 저장 버튼
        self.save_btn = QPushButton("선택한 이미지 저장")
        self.save_btn.clicked.connect(self.save_images)
        
        # 레이아웃에 위젯 추가
        layout.addWidget(self.label_info)
        layout.addLayout(file_layout)
        layout.addWidget(QLabel("추출된 이미지 목록:"))
        layout.addWidget(self.select_all_checkbox)
        layout.addWidget(self.image_list)
        layout.addLayout(zoom_layout)
        layout.addWidget(self.save_btn)
        layout.addStretch()
        
        return layout

    def setup_right_panel(self):
        layout = QVBoxLayout()
        
        # 미리보기 라벨
        preview_label = QLabel("이미지 미리보기")
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
            "PDF 문서 선택", 
            "", 
            "PDF files (*.pdf)"
        )
        if file_path:
            self.current_pdf_path = file_path
            self.file_path_label.setText(f"선택된 문서: {os.path.basename(file_path)}")
            
            # 기존 문서가 있으면 닫기
            if self.current_doc:
                self.current_doc.close()
            
            # 새 문서 열기
            self.current_doc = fitz.open(file_path)
            
            # 이미지 추출
            self.extract_images()
            
            # 이미지 목록 업데이트
            self.update_image_list()
            
            # 첫 번째 이미지 미리보기 표시
            if self.image_list.count() > 0:
                self.image_list.setCurrentRow(0)

    def extract_images(self):
        self.images = []
        
        for page_num in range(self.current_doc.page_count):
            page = self.current_doc[page_num]
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = self.current_doc.extract_image(xref)
                image_bytes = base_image["image"]
                
                # 이미지 정보 저장
                image_info = {
                    'page': page_num + 1,
                    'index': img_index + 1,
                    'data': image_bytes,
                    'ext': base_image["ext"]
                }
                self.images.append(image_info)

    def update_image_list(self):
        self.image_list.clear()
        
        for i, img in enumerate(self.images):
            item = QListWidgetItem(f"페이지 {img['page']} - 이미지 {img['index']} ({img['ext']})")
            item.setData(Qt.UserRole, i)  # 이미지 인덱스 저장
            self.image_list.addItem(item)
            
        # 이미지 목록이 업데이트되면 체크박스 상태 초기화
        self.select_all_checkbox.setChecked(False)

    def show_image(self, current, previous=None):
        if not current:  # 선택된 항목이 없으면 리턴
            return
            
        # 기존 미리보기 제거
        for i in reversed(range(self.preview_layout.count())):
            widget = self.preview_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        # 선택된 이미지 표시
        img_index = current.data(Qt.UserRole)
        img_info = self.images[img_index]
        
        # 이미지 데이터를 PIL Image로 변환
        image = Image.open(io.BytesIO(img_info['data']))
        
        # PIL Image를 QPixmap으로 변환
        img_data = image.convert("RGBA").tobytes("raw", "RGBA")
        qim = QImage(img_data, image.size[0], image.size[1], QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(qim)
        
        # 이미지 크기 조정 (배율 적용)
        zoom = self.zoom_spin.value() / 100
        scaled_pixmap = pixmap.scaled(int(pixmap.width() * zoom), int(pixmap.height() * zoom),
                                      Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        # 라벨에 이미지 표시
        label = QLabel()
        label.setPixmap(scaled_pixmap)
        label.setAlignment(Qt.AlignCenter)
        
        # 이미지 정보 표시
        info_label = QLabel(f"페이지 {img_info['page']} - 이미지 {img_info['index']}\n"
                          f"크기: {image.size[0]}x{image.size[1]}")
        info_label.setAlignment(Qt.AlignCenter)
        
        # 컨테이너에 추가
        self.preview_layout.addWidget(info_label)
        self.preview_layout.addWidget(label)

    def save_images(self):
        selected_items = self.image_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "경고", "저장할 이미지를 선택해주세요.")
            return
            
        # 원본 파일의 경로와 파일명 분리
        original_dir = os.path.dirname(self.current_pdf_path)
        original_filename = os.path.basename(self.current_pdf_path)
        
        # 새 폴더명 생성 (원본파일명_images)
        default_dir_name = os.path.splitext(original_filename)[0] + '_images'
        # 전체 경로 생성 (원본경로/원본파일명_images)
        default_save_dir = os.path.join(original_dir, default_dir_name)
        
        save_dir = QFileDialog.getExistingDirectory(
            self, 
            "저장 폴더 선택",
            default_save_dir  # 원본 파일 경로를 기본 저장 경로로 설정
        )
        
        if save_dir:
            try:
                for item in selected_items:
                    img_index = item.data(Qt.UserRole)
                    img_info = self.images[img_index]
                    
                    # 파일명 생성
                    filename = f"page{img_info['page']}_image{img_info['index']}.{img_info['ext']}"
                    save_path = os.path.join(save_dir, filename)
                    
                    # 이미지 저장
                    with open(save_path, 'wb') as f:
                        f.write(img_info['data'])
                
                QMessageBox.information(self, "성공", "선택한 이미지가 성공적으로 저장되었습니다.")
            except Exception as e:
                QMessageBox.critical(self, "오류", f"이미지 저장 중 오류가 발생했습니다: {str(e)}")

    def closeEvent(self, event):
        if self.current_doc:
            self.current_doc.close()
        super().closeEvent(event)

    def toggle_select_all(self, state):
        if state == Qt.Checked:
            self.image_list.selectAll()
        else:
            self.image_list.clearSelection() 