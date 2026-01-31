<p align="center">
  <img src="https://doctr-static.mindee.com/hwte/raw/main/docs/images/Logo_hwte.gif" width="40%">
</p>

# CraftIQ OCR
### by **Ns Akash** (@craftiq)

**CraftIQ OCR** is a Streamlit-based OCR demo built using the open-source **HWTE** OCR engine.

---

## ✨ Features
- End-to-End OCR (text detection + text recognition)
- Works with PDF and Images
- Streamlit UI for quick testing
- Export recognized text into structured format

---

## 🚀 Run Locally

### 1) Install dependencies

```bash
pip install -r demo/pt-requirements.txt
```

### 2) Run Streamlit

```bash
streamlit run demo/app.py
```

> Models will download automatically when first used.

---

## 🧠 Example Usage (Python)

```python
from hwte.io import DocumentFile
from hwte.models import ocr_predictor

model = ocr_predictor(pretrained=True)
doc = DocumentFile.from_pdf("path/to/your/doc.pdf")
result = model(doc)

# Export JSON
json_output = result.export()
```

---

## 🙏 Credits
This project is based on the open-source **Doctr** OCR library originally developed by Mindee.

---

## 📜 License
This repository is released under a general open-source license for learning and demo purposes.

---

## © Copyright
© 2026 **CraftIQ** — **Ns Akash**. All rights reserved.
