# PDF Composer 릴리즈 노트

## v1.1.0 (2024-04-11)

### 새로운 기능
- PDF A4 포매팅 기능 추가
  - PDF 문서를 A4 용지 크기에 맞게 자동 조정
  - 드래그 앤 드롭으로 파일 추가 지원
  - 사용자 지정 저장 위치 지원
 - PDF 미리보기 확대/축소 기능 추가

### 개선사항
- PDF 회전 기능 성능 개선
- PDF 분할 기능 안정성 향상
- 이미지 추출 품질 개선

### 버그 수정
- PDF to JPEG 변환 시 일부 페이지 누락 문제 해결
- 수식 추출 시 특수 문자 인식 오류 수정
- 메모리 누수 문제 해결

### 시스템 요구사항
- Python 3.8 이상
- PyQt5
- PyPDF2
- fitz (PyMuPDF)

### 설치 방법
```bash
pip install -r requirements.txt
```

### 다운로드
- [GitHub 릴리즈 페이지](https://github.com/Seobuk/PDF_tools/releases/tag/v1.1.0)에서 다운로드 가능

### 최신 버전 다운로드
- [GitHub 릴리즈 페이지](https://github.com/Seobuk/PDF_tools/releases/tag/v1.2.0)에서 다운로드 가능

### 알려진 이슈
- 일부 특수 문자를 포함한 PDF 문서에서 수식 추출 시 오류가 발생할 수 있습니다.
- 매우 큰 PDF 파일(100MB 이상) 처리 시 성능 저하가 발생할 수 있습니다.

### 이전 버전에서 업데이트하는 방법
1. 기존 설치된 버전 제거
2. 새로운 버전 설치
3. 설정 파일 백업 후 복원 (필요한 경우)

### 문의 및 지원
- GitHub Issues: https://github.com/Seobuk/PDF_tools/issues
- 이메일: [이메일 주소]

## v1.2.0 (2024-05-22)

### 변경 사항
- 어두운 테마가 기본 적용되어 UI가 더욱 세련되게 개선되었습니다.
- 실행 파일(exe) 생성 방법을 README에 추가했습니다.
- 종속성 목록에 `pyinstaller`가 추가되었습니다.

