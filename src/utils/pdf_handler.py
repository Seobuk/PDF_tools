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
                    temp_pdf = self.image_to_pdf(file_path)
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

    def image_to_pdf(self, image_path, output_path=None):
        """이미지 파일을 PDF로 변환한다.

        Parameters
        ----------
        image_path : str
            변환할 이미지 경로
        output_path : str, optional
            저장할 PDF 경로. 지정하지 않으면 임시 파일을 생성한다.

        Returns
        -------
        str
            생성된 PDF 파일의 경로
        """

        if output_path is None:
            temp_fd, output_path = tempfile.mkstemp(suffix='.pdf')
            os.close(temp_fd)

        try:
            with Image.open(image_path) as image:
                if image.mode == 'RGBA':
                    image = image.convert('RGB')
                image.save(output_path, "PDF", resolution=100.0)
        except Exception as e:
            if os.path.exists(output_path):
                os.remove(output_path)
            raise e

        return output_path
