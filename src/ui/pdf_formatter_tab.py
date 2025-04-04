from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                           QFileDialog, QLabel, QProgressBar)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from PyPDF2 import PdfReader, PdfWriter
import os

class DropArea(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n여기에 PDF 파일을 드래그하세요\n또는 클릭하여 파일을 선택하세요')
        self.setStyleSheet('''
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 5px;
                background-color: #f0f0f0;
                padding: 20px;
            }
            QLabel:hover {
                background-color: #e0e0e0;
            }
        ''')
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls() and event.mimeData().urls()[0].toLocalFile().endswith('.pdf'):
            event.acceptProposedAction()
            self.setStyleSheet('''
                QLabel {
                    border: 2px dashed #4CAF50;
                    border-radius: 5px;
                    background-color: #E8F5E9;
                    padding: 20px;
                }
            ''')

    def dragLeaveEvent(self, event):
        self.setStyleSheet('''
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 5px;
                background-color: #f0f0f0;
                padding: 20px;
            }
            QLabel:hover {
                background-color: #e0e0e0;
            }
        ''')

    def dropEvent(self, event: QDropEvent):
        file_path = event.mimeData().urls()[0].toLocalFile()
        self.parent().handleDroppedFile(file_path)
        self.setStyleSheet('''
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 5px;
                background-color: #f0f0f0;
                padding: 20px;
            }
            QLabel:hover {
                background-color: #e0e0e0;
            }
        ''')

class PdfFormatterTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        # 드래그 앤 드롭 영역
        self.dropArea = DropArea(self)
        self.dropArea.mousePressEvent = self.selectFile  # 클릭으로도 파일 선택 가능
        
        # 선택된 파일 경로 표시
        self.fileLabel = QLabel('선택된 파일: 없음')
        
        # 변환 버튼
        self.convertButton = QPushButton('A4 형식으로 변환')
        self.convertButton.clicked.connect(self.convertToA4)
        self.convertButton.setEnabled(False)
        
        # 진행 상태바
        self.progressBar = QProgressBar()
        self.progressBar.setVisible(False)
        
        # 위젯 배치
        layout.addWidget(self.dropArea)
        layout.addWidget(self.fileLabel)
        layout.addWidget(self.convertButton)
        layout.addWidget(self.progressBar)
        
        self.setLayout(layout)

    def handleDroppedFile(self, file_path):
        if file_path.lower().endswith('.pdf'):
            self.selected_file = file_path
            self.fileLabel.setText(f'선택된 파일: {file_path}')
            self.convertButton.setEnabled(True)
            self.dropArea.setText('PDF 파일이 선택되었습니다\n다른 파일을 드래그하여 변경할 수 있습니다')

    def selectFile(self, event=None):
        fname, _ = QFileDialog.getOpenFileName(self, '파일 선택', '', 
                                             'PDF 파일 (*.pdf)')
        if fname:
            self.handleDroppedFile(fname)

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
                
            except Exception as e:
                self.fileLabel.setText(f'오류 발생: {str(e)}')
            finally:
                self.progressBar.setVisible(False) 