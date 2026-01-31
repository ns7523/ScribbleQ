Sure Ns ✅ here is the full README.md in proper Markdown (.md) format for your ScribbleQ (HWTE) project (final version).

Copy-paste directly into README.md:

<p align="center">
  <img src="https://doctr-static.mindee.com/hwte/raw/main/docs/images/Logo_hwte.gif" width="40%">
</p>

# ScribbleQ (HWTE)
### Handwritten Text Extraction & Digitization  
**by Ns Akash (@craftiq)**

**ScribbleQ (HWTE)** is a Streamlit-based handwritten OCR application that extracts handwritten text from **PDFs and Images** and converts it into editable digital text.

---

## 🚀 Live Demo

[![Open Live Demo](https://img.shields.io/badge/🚀%20Open%20Live%20Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://scribbleq.streamlit.app)

---

## ✨ Features
- End-to-End OCR (**Text Detection + Text Recognition**)
- Supports **PDF** and **Image** uploads (JPG / PNG / JPEG)
- Streamlit UI for quick testing and usage
- Display OCR output as structured JSON
- Export recognized text in **TXT** and **PDF**
- Translation support (optional)

---

## 🛠 Tech Stack
- Python
- Streamlit
- PyTorch
- HWTE / Doctr OCR Engine
- OpenCV, NumPy, Matplotlib
- fpdf2 (PDF export)
- googletrans (translation)

---

## 📂 Project Structure

```text
scribbleq/
├── streamlit_app.py
├── requirements.txt
├── demo/
│   ├── app.py
│   ├── DejaVuSans.ttf
│   ├── backend/
│   │   └── pytorch.py
├── hwte/
└── README.md


⸻

🚀 Run Locally

1) Install dependencies

pip install -r requirements.txt

2) Run Streamlit

streamlit run streamlit_app.py

Pretrained models will download automatically the first time you run OCR.

⸻

🧠 Example Usage (Python)

from hwte.io import DocumentFile
from hwte.models import ocr_predictor

model = ocr_predictor(pretrained=True)
doc = DocumentFile.from_pdf("path/to/your/doc.pdf")

result = model(doc)

# Export JSON structured output
json_output = result.export()
print(json_output)


⸻

🙏 Credits

This project is built using the open-source HWTE / Doctr OCR library originally developed by Mindee.

⸻

📜 License / Usage Policy

This repository is published for learning and demo purposes.

This repository is proprietary. Viewing is permitted, copying/modifying/redistributing is not allowed without written permission.

⸻

© Copyright

© 2026 CraftIQ — Ns Akash. All rights reserved.

If you want, I can also add:
✅ screenshots section  
✅ “How it works” diagram section  
✅ IEEE paper citation block
