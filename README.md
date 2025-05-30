# PDF Composer

v1.2.0

PDF 문서를 편집하고 변환할 수 있는 PyQt5 기반의 데스크톱 애플리케이션입니다.
기본적으로 세련된 다크 테마를 적용하여 더욱 편안한 사용 경험을 제공합니다.

## 주요 기능

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

1. PDF 회전
   - PDF 파일을 선택하고 회전할 페이지를 지정
   - 90도 왼쪽/오른쪽 회전 버튼으로 회전
   - 변경사항 저장

2. PDF 분할
   - PDF 파일을 선택하고 분할할 페이지 범위 지정
   - 분할 버튼으로 새로운 PDF 생성

3. PDF to JPEG
   - PDF 파일을 선택하고 변환할 페이지 범위 지정
   - JPEG 품질 설정 후 변환

4. 수식 추출
   - PDF 파일을 선택하고 수식 형식 선택
   - 추출된 수식 목록에서 저장할 수식 선택
   - 저장 버튼으로 수식 저장

5. 이미지 추출
   - PDF 파일을 선택하고 추출할 이미지 선택
   - 저장 버튼으로 이미지 저장

6. PDF A4 포매팅
   - PDF 파일을 드래그 앤 드롭 또는 선택
   - A4 형식으로 변환 버튼 클릭
   - 저장 위치 선택

## 개발 환경

- Python 3.8+
- PyQt5
- PyPDF2
- fitz (PyMuPDF)
- pyinstaller

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
