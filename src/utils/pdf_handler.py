import fitz
from PIL import Image
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QPushButton, QLabel, QFileDialog)
from PyPDF2 import PdfMerger
import tempfile

class PDFHandler:
    @staticmethod
    def split_pdf(input_path, output_path, start_page, end_page):
        try:
            doc = fitz.open(input_path)
            new_doc = fitz.open()
            new_doc.insert_pdf(doc, from_page=start_page-1, to_page=end_page-1)
            new_doc.save(output_path)
            new_doc.close()
            doc.close()
            return True
        except Exception as e:
            raise Exception(f"PDF 쪼개기 실패: {str(e)}")

    def combine_pdfs(self, file_paths, output_path):
        merger = PdfMerger()
        temp_files = []  # 임시 파일 목록 관리
        
        try:
            for file_path in file_paths:
                ext = os.path.splitext(file_path)[1].lower()
                
                if ext == '.pdf':
                    merger.append(file_path)
                elif ext in ['.jpg', '.jpeg', '.png']:
                    # 이미지를 PDF로 변환
                    temp_pdf = self._convert_image_to_pdf(file_path)
                    temp_files.append(temp_pdf)  # 임시 파일 목록에 추가
                    merger.append(temp_pdf)
            
            # 기존 파일이 있다면 삭제
            if os.path.exists(output_path):
                os.remove(output_path)
                
            merger.write(output_path)
            
        except Exception as e:
            raise e
        
        finally:
            merger.close()
            # 임시 파일들 삭제
            for temp_file in temp_files:
                try:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                except:
                    pass

    def _convert_image_to_pdf(self, image_path):
        # 시스템 임시 디렉토리에 임시 파일 생성
        temp_fd, temp_pdf = tempfile.mkstemp(suffix='.pdf')
        os.close(temp_fd)  # 파일 디스크립터 즉시 닫기
        
        try:
            with Image.open(image_path) as image:
                # RGBA 이미지를 RGB로 변환
                if image.mode == 'RGBA':
                    image = image.convert('RGB')
                image.save(temp_pdf, "PDF", resolution=100.0)
        except Exception as e:
            if os.path.exists(temp_pdf):
                os.remove(temp_pdf)
            raise e
            
        return temp_pdf

    @staticmethod
    def image_to_pdf(img):
        # 이미지를 PDF로 변환하는 로직
        pass

    def image_to_pdf(self, img_path):
        from PIL import Image  # 필요할 때만 import
        # ... 나머지 코드 