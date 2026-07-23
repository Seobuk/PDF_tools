<div align="center">

# 📄 PDF Composer

**An all-in-one desktop tool for PDF editing — merge · split · rotate · convert · extract**

[![Release](https://img.shields.io/github/v/release/Seobuk/PDF_tools?label=Release&color=2ea44f)](https://github.com/Seobuk/PDF_tools/releases/latest)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/GUI-PyQt5-41CD52?logo=qt&logoColor=white)](https://pypi.org/project/PyQt5/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Want to use it without installing? → **[Download the latest release](https://github.com/Seobuk/PDF_tools/releases/latest)**

🌐 **English** · [한국어](README.ko.md)

</div>

---

## ✨ Features at a Glance

| Tab | What it does | Highlights |
|---|---|---|
| 📑 **Merge PDFs** | Combine multiple PDFs and images into one PDF | Drag & drop, reorder, supports JPG/PNG/BMP/TIFF/WEBP/GIF, automatic EXIF rotation correction |
| ✂️ **Split PDF** | Save a page range as a new PDF | Live preview to confirm the range |
| 🖼️ **PDF → Image** | Export pages as PNG/JPEG | High-resolution 300 DPI output |
| 🔄 **Rotate PDF** | Rotate pages in 90° steps | Click to multi-select in the preview, refreshes only the selected pages instantly |
| 🧲 **Extract Images** | Pull embedded images out of a document as-is | Select all, preserves the original format (jpeg/png, etc.) |
| 📐 **A4 Formatting** | Normalize inconsistent page sizes to A4 | Side-by-side before/after preview |

Every preview supports zoom in/out with **Ctrl + Mouse Wheel**.

---

## 🚀 Getting Started

### Option 1 — Executable (Windows)

Download `PDF_Tools-windows.zip` from the [releases page](https://github.com/Seobuk/PDF_tools/releases/latest), extract it, then run `PDF_Tools.exe` inside the extracted `PDF_Tools` folder. No installation required.

> Keep `PDF_Tools.exe` next to its `_internal` folder — the app won't start if you move the exe out on its own.

### Option 2 — Run from source

```bash
git clone https://github.com/Seobuk/PDF_tools.git
cd PDF_tools
pip install -r requirements.txt
python main.py
```

### Build the exe yourself (optional)

```bash
pyinstaller --noconsole --onedir --name PDF_Tools main.py
```

---

## 📸 Feature Tour

### 📑 Merge PDFs

Add PDFs and images (JPG/PNG/BMP/TIFF/WEBP/GIF) by dragging them in or using the "Add File" button,
reorder them with the mouse, and press "Create PDF" to merge everything into a single PDF.
EXIF rotation from phone photos is corrected automatically. (Press Delete to remove an item.)

![Merge PDFs](docs/screenshots/01_merge.png)

### ✂️ Split PDF

Select a PDF and specify the page range to split, confirming your selection with the live preview.

![Split PDF](docs/screenshots/02_split.png)

### 🖼️ PDF → Image

Specify the page range and image format (PNG/JPEG) to save pages as high-resolution 300 DPI images.

![PDF to Image](docs/screenshots/03_to_image.png)

### 🔄 Rotate PDF

Click pages in the preview to select them (blue outline), rotate them left/right by 90°, and save.
You can select multiple pages and rotate them all at once.

![Rotate PDF](docs/screenshots/04_rotate.png)

### 🧲 Extract Images

List the images embedded in a PDF and save the selected ones in their original format.

![Extract Images](docs/screenshots/05_extract.png)

### 📐 A4 Formatting

Convert PDFs with inconsistent sizes (e.g. landscape documents) to fit A4, with a side-by-side before/after preview.

![A4 Formatting](docs/screenshots/06_a4_format.png)

---

## 🗂️ Project Structure

```
PDF_tools/
├── main.py                       # App entry point (applies Fusion style)
├── requirements.txt
├── docs/screenshots/             # README screenshots
└── src/
    ├── ui/
    │   ├── main_window.py            # Tab-based main window
    │   ├── pdf_combiner.py           # 📑 Merge PDFs/images
    │   ├── pdf_splitter.py           # ✂️ Split by page range
    │   ├── pdf_to_image.py           # 🖼️ PDF → PNG/JPEG
    │   ├── pdf_rotator.py            # 🔄 Rotate pages
    │   ├── pdf_image_extractor.py    # 🧲 Extract embedded images
    │   ├── pdf_formatter_tab.py      # 📐 A4 formatting
    │   ├── preview.py                # Shared preview helpers (rendering/scaling/panels)
    │   ├── zoomable_scroll_area.py   # Ctrl+wheel zoomable scroll area
    │   └── styles.py                 # Shared style constants
    └── utils/
        └── pdf_handler.py            # Merge / image→PDF conversion logic
```

## 🛠️ Tech Stack

| Role | Library |
|---|---|
| GUI | [PyQt5](https://pypi.org/project/PyQt5/) (Fusion style) |
| PDF rendering / rotation / splitting | [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) |
| PDF merging / A4 conversion | [PyPDF2](https://pypdf2.readthedocs.io/) |
| Image processing | [Pillow](https://pillow.readthedocs.io/) |
| Executable build | [PyInstaller](https://pyinstaller.org/) |

Releases are automated with GitHub Actions — when `.release-trigger` changes on the `main` branch,
a tag is created, release notes are published (based on [RELEASE_NOTES.md](RELEASE_NOTES.md)), and the Windows exe is built and uploaded automatically.

## 📄 License

This project is distributed under the [MIT License](https://opensource.org/licenses/MIT).

<div align="center">

Made by **SHU** · Report bugs and suggest features on [Issues](https://github.com/Seobuk/PDF_tools/issues) 🙌

</div>
