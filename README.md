# PDF Composer

v1.4.0

PDF 문서를 편집하고 변환할 수 있는 PyQt5 기반의 데스크톱 애플리케이션입니다.
군더더기 없는 Qt 기본(Fusion) 디자인으로 어떤 환경에서도 깨짐 없이 동작합니다.

## 주요 기능

- PDF 병합: PDF와 이미지(JPG/PNG/BMP/TIFF/WEBP/GIF)를 원하는 순서로 한 PDF로 병합
- PDF 회전: PDF 페이지를 90도 단위로 회전
- PDF 분할: PDF 문서를 페이지 단위로 분할
- PDF to JPEG: PDF 페이지를 JPEG 이미지로 변환
- 수식 추출: PDF 문서에서 수식을 추출하여 저장
- 이미지 추출: PDF 문서에서 이미지를 추출하여 저장
- PDF A4 포매팅: PDF 내용을 A4 용지 크기에 맞게 조정
- 미리보기 확대/축소 지원

## 설치 방법

1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

2. 애플리케이션 실행:
```bash
python main.py
```

3. 실행 파일(exe) 생성 (선택 사항):
```bash
pyinstaller --noconsole --onefile main.py
```

## 사용 방법

### 1. PDF 병합

PDF와 이미지(JPG/PNG/BMP/TIFF/WEBP/GIF)를 드래그하거나 '파일 추가' 버튼으로 추가한 뒤,
마우스로 순서를 조정하고 'PDF 생성'을 누르면 하나의 PDF로 병합됩니다.

![PDF 병합](docs/screenshots/01_merge.png)

### 2. PDF 분할

PDF 파일을 선택하고 분할할 페이지 범위를 지정하면 미리보기로 확인하면서 분할할 수 있습니다.

![PDF 분할](docs/screenshots/02_split.png)

### 3. PDF → 이미지 변환

변환할 페이지 범위와 이미지 형식(PNG/JPEG)을 지정해 페이지를 이미지로 저장합니다.

![PDF 이미지 변환](docs/screenshots/03_to_image.png)

### 4. PDF 회전

미리보기에서 페이지를 클릭해 선택(파란 테두리)하고 90도 왼쪽/오른쪽 버튼으로 회전한 뒤 저장합니다.

![PDF 회전](docs/screenshots/04_rotate.png)

### 5. 이미지 추출

PDF에 포함된 이미지를 목록으로 추출하고, 선택한 이미지를 원본 형식 그대로 저장합니다.

![이미지 추출](docs/screenshots/05_extract.png)

### 6. PDF A4 포매팅

가로 문서 등 규격이 제각각인 PDF를 A4 크기에 맞게 변환하고, 변환 전/후를 나란히 미리볼 수 있습니다.

![PDF A4 변환](docs/screenshots/06_a4_format.png)

## 개발 환경

- Python 3.8+
- PyQt5
- PyPDF2
- fitz (PyMuPDF)
- pyinstaller

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
