from PIL import Image, ImageOps
import os
from PyPDF2 import PdfMerger
import tempfile

# 병합 시 PDF로 변환해 붙일 수 있는 이미지 확장자
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.webp', '.gif'}


def default_output_path(input_path, suffix):
    """원본 파일 옆에 '원본이름 + suffix' 형태의 기본 저장 경로를 만든다."""
    base, _ = os.path.splitext(input_path)
    return base + suffix


class PDFHandler:
    def combine_pdfs(self, file_paths, output_path):
        merger = PdfMerger()
        temp_files = []  # 임시 파일 목록 관리
        
        try:
            for file_path in file_paths:
                ext = os.path.splitext(file_path)[1].lower()
                
                if ext == '.pdf':
                    merger.append(file_path)
                elif ext in IMAGE_EXTENSIONS:
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
                # 휴대폰 사진 등의 EXIF 회전 정보를 실제 픽셀에 반영
                image = ImageOps.exif_transpose(image)
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                image.save(output_path, "PDF", resolution=100.0)
        except Exception as e:
            if os.path.exists(output_path):
                os.remove(output_path)
            raise e

        return output_path
