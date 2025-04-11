from PyQt5.QtWidgets import QMainWindow, QTabWidget
from .pdf_combiner import PDFMergerWidget
from .pdf_splitter import PDFSplitterWidget
from .pdf_to_image import PDFToImageWidget
from .pdf_rotator import PDFRotatorWidget
from .pdf_image_extractor import PDFImageExtractorWidget
from .pdf_formula_extractor import PDFFormulaExtractorWidget
from .pdf_formatter_tab import PdfFormatterTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF 도구모음 (만든사람 SHU, VER 1.1)")
        self.setup_ui()

    def setup_ui(self):
        # 탭 위젯 생성
        self.tabs = QTabWidget()
        
        # 위젯 추가
        self.tabs.addTab(PDFMergerWidget(), "PDF 문서 병합")
        self.tabs.addTab(PDFSplitterWidget(), "PDF 문서 분할")
        self.tabs.addTab(PDFToImageWidget(), "PDF → 이미지 변환")
        self.tabs.addTab(PDFRotatorWidget(), "PDF 문서 회전")
        self.tabs.addTab(PDFImageExtractorWidget(), "PDF 이미지 추출")
        # self.tabs.addTab(PDFFormulaExtractorWidget(), "PDF 수식 추출")
        
        # PDF 포매터 탭 추가
        pdf_tab = PdfFormatterTab()
        self.tabs.addTab(pdf_tab, 'PDF A4 변환')
        
        self.setCentralWidget(self.tabs)
        self.setMinimumSize(800, 600) 