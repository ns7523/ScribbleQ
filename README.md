<div align="center">

<img src="assets/brand/hero.svg" alt="ScribbleQ" width="100%" />

<br />

<p>
  <strong>Digitize documents.</strong> <strong>Recognize handwritten content.</strong> <strong>Export structured text.</strong>
</p>

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" alt="PyTorch" />
  <img src="https://img.shields.io/badge/OCR-7C3AED?style=for-the-badge&logo=googledocs&logoColor=white" alt="OCR" />
</p>

</div>

---

<div align="center">

<table>
<tr>
<td align="center" width="25%"><strong>Type</strong><br />OCR Application</td>
<td align="center" width="25%"><strong>Input</strong><br />PDF / JPG / PNG</td>
<td align="center" width="25%"><strong>Output</strong><br />Text / JSON / PDF</td>
<td align="center" width="25%"><strong>Interface</strong><br />Streamlit</td>
</tr>
</table>

</div>

---

## 01 · Overview

<table>
<tr>
<td width="58%" valign="top">

### Handwritten document digitization system

**ScribbleQ** is an OCR-based document intelligence application for converting handwritten documents into clean digital text.

The system combines document input handling, text-region detection, recognition, structured output, and an interactive Streamlit interface for fast document processing.

</td>
<td width="42%" valign="top">

```text
┌──────────────────────────────┐
│  SCRIBBLEQ OCR CONSOLE       │
├──────────────────────────────┤
│  Input      PDF / Image      │
│  Detect     Text Regions     │
│  Recognize  Handwriting      │
│  Output     Text / JSON      │
│  UI         Streamlit        │
└──────────────────────────────┘
```

</td>
</tr>
</table>

---

## 02 · OCR Pipeline

<img src="assets/brand/pipeline.svg" alt="ScribbleQ OCR pipeline" width="100%" />

---

## 03 · System Architecture

```mermaid
flowchart TD
    A[PDF / Image Input] --> B[Document Loader]
    B --> C[Text Detection]
    C --> D[Text Recognition]
    D --> E[Structured Output]
    E --> F[Text Export]
    E --> G[PDF Export]
    E --> H[JSON Export]
    I[Streamlit UI] --> B
```

---

## 04 · Key Features

| Feature | Purpose |
|---|---|
| Handwritten OCR | Converts handwritten document content into digital text. |
| Multi-format input | Supports PDFs and common image formats. |
| Detection and recognition flow | Separates page analysis from text recognition for cleaner processing. |
| Structured output | Produces data that can be reused in downstream workflows. |
| Export utilities | Supports text, JSON, and PDF-oriented output paths. |
| Streamlit interface | Provides a simple interactive upload and processing experience. |

---

## 05 · AI Workflow

```mermaid
flowchart LR
    A[Document] --> B[Preprocess]
    B --> C[Detect Text Blocks]
    C --> D[Recognize Text]
    D --> E[Assemble Output]
    E --> F[Export]
```

| Stage | Output |
|---|---|
| Input loading | PDF or image document converted into processable pages. |
| Detection | Located text regions and layout blocks. |
| Recognition | Handwritten content converted into digital text. |
| Structuring | Text arranged into export-ready payloads. |
| Export | Text, JSON, or PDF output. |

---

## 06 · Installation

```bash
git clone https://github.com/ns7523/ScribbleQ.git
cd ScribbleQ
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 07 · Usage

Run the Streamlit app:

```bash
streamlit run streamlit_app.py
```

Open the local interface:

```text
http://localhost:8501
```

Python API example:

```python
from hwte.io import DocumentFile
from hwte.models import ocr_predictor

model = ocr_predictor(pretrained=True)
doc = DocumentFile.from_pdf("document.pdf")
result = model(doc)

print(result.export())
```

---

## 08 · Project Structure

```text
.
├── assets/
│   └── brand/
│       ├── hero.svg
│       └── pipeline.svg
├── demo/
│   ├── app.py
│   └── backend/
│       └── pytorch.py
├── hwte/
├── streamlit_app.py
├── requirements.txt
└── README.md
```

Suggested production structure:

```text
docs/ · demo/ · hwte/ · tests/ · examples/ · assets/screenshots/ · requirements.txt
```

---

## 09 · Visual Assets

<table>
<tr>
<td width="50%" valign="top">

### Upload Interface

`assets/screenshots/upload-interface.png`

Streamlit upload and document selection flow.

</td>
<td width="50%" valign="top">

### OCR Result

`assets/screenshots/ocr-result.png`

Recognized text output.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### Export View

`assets/screenshots/export-view.png`

Text, PDF, and JSON export options.

</td>
<td width="50%" valign="top">

### Pipeline View

`assets/screenshots/pipeline-view.png`

Visual overview of detection and recognition stages.

</td>
</tr>
</table>

---

## 10 · Future Improvements

- [ ] Add sample input and output examples.
- [ ] Add OCR accuracy and latency benchmarks.
- [ ] Add screenshots under `assets/screenshots/`.
- [ ] Add deployment notes for Streamlit Cloud.
- [ ] Add tests for input loading and export utilities.
- [ ] Add documentation for OCR model components.
- [ ] Add a clear license file.

---

<div align="center">

### N S Akash

**AI & Cybersecurity Engineer**

<p>
  <a href="https://github.com/ns7523"><img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" /></a>
  <a href="https://nsakash.in"><img src="https://img.shields.io/badge/Portfolio-0A84FF?style=for-the-badge&logo=safari&logoColor=white" alt="Portfolio" /></a>
  <a href="mailto:contact@nsakash.in"><img src="https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" /></a>
  <a href="https://www.linkedin.com/in/nsakash7523"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
</p>

</div>
