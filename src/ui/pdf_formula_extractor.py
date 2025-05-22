from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFileDialog, QMessageBox, QListWidget,
    QTextEdit, QComboBox, QSpinBox, QCheckBox, QApplication
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QClipboard
import fitz
import re
import os

class PDFFormulaExtractorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.current_doc = None
        self.current_pdf_path = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # 설명 라벨
        self.label_info = QLabel("PDF 문서에서 수식을 추출하여 저장할 수 있습니다.\n"
                                "수식을 선택하고 저장할 폴더를 지정하세요.")
        self.label_info.setWordWrap(True)
        
        # 파일 선택 영역
        file_layout = QHBoxLayout()
        self.file_path_label = QLabel("선택된 문서: 없음")
        self.file_path_label.setWordWrap(True)
        self.select_file_btn = QPushButton("PDF 문서 선택")
        self.select_file_btn.clicked.connect(self.select_pdf)
        file_layout.addWidget(self.file_path_label)
        file_layout.addWidget(self.select_file_btn)
        
        # 수식 검색 옵션
        options_layout = QHBoxLayout()
        
        # 수식 형식 선택
        self.formula_type = QComboBox()
        self.formula_type.addItems(["모든 수식", "LaTeX 수식", "수학 기호", "분수", "적분", "행렬"])
        self.formula_type.currentTextChanged.connect(self.update_formula_list)
        
        # 페이지 범위 선택
        self.start_page = QSpinBox()
        self.start_page.setMinimum(1)
        self.start_page.setMaximum(9999)
        self.start_page.valueChanged.connect(self.update_formula_list)
        
        self.end_page = QSpinBox()
        self.end_page.setMinimum(1)
        self.end_page.setMaximum(9999)
        self.end_page.valueChanged.connect(self.update_formula_list)
        
        # 수식 포함 옵션
        self.include_context = QCheckBox("문맥 포함")
        self.include_context.setChecked(True)
        self.include_context.stateChanged.connect(self.update_formula_list)
        
        options_layout.addWidget(QLabel("수식 형식:"))
        options_layout.addWidget(self.formula_type)
        options_layout.addWidget(QLabel("페이지:"))
        options_layout.addWidget(self.start_page)
        options_layout.addWidget(QLabel("~"))
        options_layout.addWidget(self.end_page)
        options_layout.addWidget(self.include_context)
        
        # 수식 목록
        self.formula_list = QListWidget()
        self.formula_list.itemClicked.connect(self.show_formula)
        self.formula_list.currentItemChanged.connect(self.show_formula)
        
        # 저장 버튼
        self.save_btn = QPushButton("선택한 수식 저장")
        self.save_btn.clicked.connect(self.save_formulas)
        
        # 레이아웃에 위젯 추가
        layout.addWidget(self.label_info)
        layout.addLayout(file_layout)
        layout.addLayout(options_layout)
        layout.addWidget(QLabel("추출된 수식 목록:"))
        layout.addWidget(self.formula_list)
        layout.addWidget(self.save_btn)
        layout.addStretch()
        
        self.setLayout(layout)

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
            
            # 페이지 범위 설정
            self.start_page.setMaximum(self.current_doc.page_count)
            self.end_page.setMaximum(self.current_doc.page_count)
            self.end_page.setValue(self.current_doc.page_count)
            
            # 수식 추출
            self.extract_formulas()
            
            # 수식 목록 업데이트
            self.update_formula_list()
            
            # 첫 번째 수식 미리보기 표시
            if self.formula_list.count() > 0:
                self.formula_list.setCurrentRow(0)

    def extract_formulas(self):
        self.formulas = []
        
        if not self.current_doc:
            return
            
        start_page = max(1, self.start_page.value()) - 1
        end_page = min(self.current_doc.page_count, self.end_page.value())
        
        for page_num in range(start_page, end_page):
            page = self.current_doc[page_num]
            
            # 텍스트 추출
            text = page.get_text()
            
            # 수식 패턴 매칭
            patterns = {
                "모든 수식": r'[∫∑∏√±×÷=≠≈≤≥∈∉⊂⊃∪∩]|[a-zA-Z]+\s*=\s*[^=]',
                "LaTeX 수식": r'\$[^$]+\$|\\\([^)]+\\\)|\\\[[^\]]+\\\]',
                "수학 기호": r'[∫∑∏√±×÷=≠≈≤≥∈∉⊂⊃∪∩]',
                "분수": r'\\frac{[^}]+}{[^}]+}|[0-9]+/[0-9]+',
                "적분": r'∫[^∫]+∫|\\int[^\\]+\\int',
                "행렬": r'\\begin{matrix}[^\\]+\\end{matrix}'
            }
            
            pattern = patterns.get(self.formula_type.currentText(), patterns["모든 수식"])
            matches = re.finditer(pattern, text)
            
            for match in matches:
                formula = match.group()
                context = ""
                
                if self.include_context.isChecked():
                    # 문맥 추출 (앞뒤 50자)
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 50)
                    context = text[start:end]
                
                self.formulas.append({
                    'page': page_num + 1,
                    'formula': formula,
                    'context': context
                })

    def update_formula_list(self):
        self.formula_list.clear()
        
        if not self.current_doc:
            return
            
        self.extract_formulas()
        
        for i, formula_info in enumerate(self.formulas):
            item = QListWidgetItem(f"페이지 {formula_info['page']} - {formula_info['formula'][:30]}...")
            item.setData(Qt.UserRole, i)
            self.formula_list.addItem(item)

    def show_formula(self, current, previous=None):
        if not current:
            self.copy_latex_btn.setEnabled(False)
            return
            
        formula_index = current.data(Qt.UserRole)
        formula_info = self.formulas[formula_index]
        
        preview_text = f"페이지: {formula_info['page']}\n\n"
        preview_text += f"수식: {formula_info['formula']}\n\n"
        
        if formula_info['context']:
            preview_text += f"문맥:\n{formula_info['context']}"
            
        self.preview_text.setText(preview_text)
        self.copy_latex_btn.setEnabled(True)

    def copy_latex(self):
        current_item = self.formula_list.currentItem()
        if not current_item:
            return
            
        formula_index = current_item.data(Qt.UserRole)
        formula_info = self.formulas[formula_index]
        
        # LaTeX 수식 추출
        latex = formula_info['formula']
        
        # LaTeX 수식이 아닌 경우 변환
        if not latex.startswith('\\') and not latex.startswith('$'):
            # 일반 수학 기호를 LaTeX로 변환
            latex = latex.replace('∫', '\\int')
            latex = latex.replace('∑', '\\sum')
            latex = latex.replace('∏', '\\prod')
            latex = latex.replace('√', '\\sqrt')
            latex = latex.replace('±', '\\pm')
            latex = latex.replace('×', '\\times')
            latex = latex.replace('÷', '\\div')
            latex = latex.replace('≠', '\\neq')
            latex = latex.replace('≈', '\\approx')
            latex = latex.replace('≤', '\\leq')
            latex = latex.replace('≥', '\\geq')
            latex = latex.replace('∈', '\\in')
            latex = latex.replace('∉', '\\notin')
            latex = latex.replace('⊂', '\\subset')
            latex = latex.replace('⊃', '\\supset')
            latex = latex.replace('∪', '\\cup')
            latex = latex.replace('∩', '\\cap')
            
            # 분수 변환
            if '/' in latex:
                latex = latex.replace('/', '}{')
                latex = '\\frac{' + latex + '}'
        
        # 클립보드에 복사
        clipboard = QApplication.clipboard()
        clipboard.setText(latex)
        
        QMessageBox.information(self, "성공", "LaTeX 수식이 클립보드에 복사되었습니다.")

    def save_formulas(self):
        selected_items = self.formula_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "경고", "저장할 수식을 선택해주세요.")
            return
            
        # 원본 파일의 경로와 파일명 분리
        original_dir = os.path.dirname(self.current_pdf_path)
        original_filename = os.path.basename(self.current_pdf_path)
        
        # 새 폴더명 생성 (원본파일명_formulas)
        default_dir_name = os.path.splitext(original_filename)[0] + '_formulas'
        # 전체 경로 생성 (원본경로/원본파일명_formulas)
        default_save_dir = os.path.join(original_dir, default_dir_name)
        
        save_dir = QFileDialog.getExistingDirectory(
            self, 
            "저장 폴더 선택",
            default_save_dir  # 원본 파일 경로를 기본 저장 경로로 설정
        )
        
        if save_dir:
            try:
                for item in selected_items:
                    formula_index = item.data(Qt.UserRole)
                    formula_info = self.formulas[formula_index]
                    
                    # 파일명 생성
                    filename = f"page{formula_info['page']}_formula{formula_index}.txt"
                    save_path = os.path.join(save_dir, filename)
                    
                    # 수식 저장
                    with open(save_path, 'w', encoding='utf-8') as f:
                        f.write(f"페이지: {formula_info['page']}\n")
                        f.write(f"수식: {formula_info['formula']}\n")
                        if formula_info['context']:
                            f.write(f"\n문맥:\n{formula_info['context']}")
                
                QMessageBox.information(self, "성공", "선택한 수식이 성공적으로 저장되었습니다.")
            except Exception as e:
                QMessageBox.critical(self, "오류", f"수식 저장 중 오류가 발생했습니다: {str(e)}")

    def closeEvent(self, event):
        if self.current_doc:
            self.current_doc.close()
        super().closeEvent(event) 