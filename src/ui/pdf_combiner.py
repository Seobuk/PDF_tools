from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QPushButton, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt
from ..utils.pdf_handler import PDFHandler
from PyQt5.QtCore import QMimeData
import os

class PDFMergerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.pdf_handler = PDFHandler()
        self.setup_ui()
        self.setAcceptDrops(True)

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # 설명 라벨
        self.label_info = QLabel("1. PDF, 이미지(JPG/PNG)를 드래그하여 추가하세요.\n"
                                "2. 순서를 마우스로 조정한 후 'PDF 생성'을 누르면 병합됩니다.")
        
        # 파일 리스트
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(self.file_list.SingleSelection)
        self.file_list.setDragDropMode(self.file_list.InternalMove)
        
        # PDF 생성 버튼
        self.btn_generate = QPushButton("PDF 생성")
        self.btn_generate.clicked.connect(self.generate_pdf)
        
        # 파일 리스트에 키 이벤트 연결
        self.file_list.keyPressEvent = self.handle_key_press
        
        layout.addWidget(self.label_info)
        layout.addWidget(self.file_list)
        layout.addWidget(self.btn_generate)
        
        self.setLayout(layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        for file_path in files:
            ext = os.path.splitext(file_path)[1].lower()
            if ext in ['.pdf', '.jpg', '.jpeg', '.png']:
                item = QListWidgetItem(os.path.basename(file_path))
                item.setData(Qt.UserRole, file_path)
                self.file_list.addItem(item)
            else:
                QMessageBox.warning(
                    self, 
                    "경고", 
                    f"지원하지 않는 파일 형식입니다: {os.path.basename(file_path)}"
                )

    def generate_pdf(self):
        if self.file_list.count() == 0:
            QMessageBox.warning(self, "경고", "파일을 추가해주세요.")
            return
            
        save_path, _ = QFileDialog.getSaveFileName(
            self, 
            "저장할 위치 선택", 
            "", 
            "PDF files (*.pdf)"
        )
        
        if save_path:
            try:
                file_paths = []
                for i in range(self.file_list.count()):
                    file_paths.append(self.file_list.item(i).data(Qt.UserRole))
                
                self.pdf_handler.combine_pdfs(file_paths, save_path)
                QMessageBox.information(self, "성공", "PDF 생성이 완료되었습니다.")
            except Exception as e:
                QMessageBox.critical(self, "오류", f"PDF 생성 중 오류가 발생했습니다: {str(e)}")

    def handle_key_press(self, event):
        # Delete 키가 눌렸을 때
        if event.key() == Qt.Key_Delete:
            # 현재 선택된 항목들을 가져옴
            selected_items = self.file_list.selectedItems()
            # 선택된 항목들을 삭제
            for item in selected_items:
                self.file_list.takeItem(self.file_list.row(item))
        else:
            # 다른 키 이벤트는 기본 동작 수행
            QListWidget.keyPressEvent(self.file_list, event) 