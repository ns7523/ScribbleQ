# Copyright (C) 2021-2025, CraftIQ.

# This program is licensed under the Apache License 2.0.
# See LICENSE or go to <https://opensource.org/licenses/Apache-2.0> for full license details.
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import cv2
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st # frontend
import torch
from backend.pytorch import DET_ARCHS, RECO_ARCHS, forward_image, load_predictor

from hwte.io import DocumentFile
from hwte.utils.visualization import visualize_page

forward_device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def main(det_archs, reco_archs):
    """Build a streamlit layout"""
    # Wide mode
    st.set_page_config(layout="wide")

    # Designing the interface
    st.title("ScribbleQ ")
    st.caption("Handwritten Text Extraction & Digitization (HWTE)")
    #st.markdown("Handwritten Text Extraction & Digitization (HWTE)")
    # For newline
    st.write("\n")
    # Instructions
    st.markdown("*Hint: click on the top-right corner of an image to enlarge it!*")
    # Set the columns
    cols = st.columns((1, 1, 1, 1))
    cols[0].subheader("Input page")
    cols[1].subheader("Segmentation heatmap")
    cols[2].subheader("OCR output")
    cols[3].subheader("Page recontruction")

    # Sidebar
    # File selection
    st.sidebar.title("Document Upload")
    # Choose your own image
    uploaded_file = st.sidebar.file_uploader("Upload files", type=["pdf", "png", "jpeg", "jpg"])
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".pdf"):
            doc = DocumentFile.from_pdf(uploaded_file.read())
        else:
            doc = DocumentFile.from_images(uploaded_file.read())
        page_idx = st.sidebar.selectbox("Page selection", [idx + 1 for idx in range(len(doc))]) - 1
        page = doc[page_idx]
        cols[0].image(page)

    # Model selection
    st.sidebar.title("Model selection")
    st.sidebar.markdown("**Backend**: PyTorch")
    det_arch = st.sidebar.selectbox("Text Detection model", det_archs)
    reco_arch = st.sidebar.selectbox("Text Recognition model", reco_archs)

    # For newline
    st.sidebar.write("\n")
    # Only straight pages or possible rotation
    st.sidebar.title("Parameters")
    assume_straight_pages = st.sidebar.checkbox("Assume straight pages", value=True)
    # Disable page orientation detection
    disable_page_orientation = st.sidebar.checkbox("Disable page orientation detection", value=False)
    # Disable crop orientation detection
    disable_crop_orientation = st.sidebar.checkbox("Disable crop orientation detection", value=False)
    # Straighten pages
    straighten_pages = st.sidebar.checkbox("Straighten pages", value=False)
    # Export as straight boxes
    export_straight_boxes = st.sidebar.checkbox("Export as straight boxes", value=False)
    st.sidebar.write("\n")
    # Binarization threshold
    bin_thresh = st.sidebar.slider("Binarization threshold", min_value=0.1, max_value=0.9, value=0.3, step=0.1)
    st.sidebar.write("\n")
    # Box threshold
    box_thresh = st.sidebar.slider("Box threshold", min_value=0.1, max_value=0.9, value=0.1, step=0.1)
    st.sidebar.write("\n")

    if st.sidebar.button("Analyze page"):
        if uploaded_file is None:
            st.sidebar.write("Please upload a document")

        else:
            with st.spinner("Loading model..."):
                predictor = load_predictor(
                    det_arch=det_arch,
                    reco_arch=reco_arch,
                    assume_straight_pages=assume_straight_pages,
                    straighten_pages=straighten_pages,
                    export_as_straight_boxes=export_straight_boxes,
                    disable_page_orientation=disable_page_orientation,
                    disable_crop_orientation=disable_crop_orientation,
                    bin_thresh=bin_thresh,
                    box_thresh=box_thresh,
                    device=forward_device,
                )

            with st.spinner("Analyzing..."):
                # Forward the image to the model
                seg_map = forward_image(predictor, page, forward_device)
                seg_map = np.squeeze(seg_map)
                seg_map = cv2.resize(seg_map, (page.shape[1], page.shape[0]), interpolation=cv2.INTER_LINEAR)

                # Plot the raw heatmap
                fig, ax = plt.subplots()
                ax.imshow(seg_map)
                ax.axis("off")
                cols[1].pyplot(fig)

                # Plot OCR output
                out = predictor([page])
                fig = visualize_page(out.pages[0].export(), out.pages[0].page, interactive=False, add_labels=False)
                cols[2].pyplot(fig)

                # Page reconstruction under input page
                page_export = out.pages[0].export()
                if assume_straight_pages or (not assume_straight_pages and straighten_pages):
                    img = out.pages[0].synthesize()
                    cols[3].image(img, clamp=True)

                # Display JSON
                st.markdown("\nHere are your analysis results in JSON format:")
                st.json(page_export, expanded=False)
                
                # Extract recognized text from OCR output
                recognized_text = " ".join([
                    word['value']
                    for block in page_export.get('blocks', [])
                    for line in block.get('lines', [])
                    for word in line.get('words', [])
                ])

                # Store recognized text in session_state for persistence
                st.session_state["recognized_text"] = recognized_text

                if not st.session_state["recognized_text"].strip():
                    st.warning("No text detected to export or translate.")

    # Persistent UI for recognized text and translation
    if "recognized_text" not in st.session_state:
        st.session_state["recognized_text"] = ""

    if "translated_text" not in st.session_state:
        st.session_state["translated_text"] = ""

    if st.session_state["recognized_text"].strip():
        st.subheader("🧾 Extracted Text")
        st.text_area("Recognized Output", st.session_state["recognized_text"], height=200)

        from googletrans import Translator
        from fpdf import FPDF  # fpdf2 is compatible with this import
        import io

        # NOTE: Download and place DejaVuSans.ttf in your project directory for full Unicode support.
        def create_pdf(text, title="Extracted Text"):
            import os
            pdf = FPDF()
            pdf.add_page()
            font_path = "DejaVuSans.ttf"
            if os.path.exists(font_path):
                pdf.add_font("DejaVu", "", font_path, uni=True)
                pdf.set_font("DejaVu", size=12)
            else:
                pdf.set_font("Helvetica", size=12)
            pdf.multi_cell(0, 10, text)

            # fpdf.output(dest="S") may return str, bytes, or bytearray depending on version
            raw = pdf.output(dest="S")
            if isinstance(raw, str):
                pdf_bytes = raw.encode('latin1', errors='ignore')
            elif isinstance(raw, bytearray):
                pdf_bytes = bytes(raw)
            else:
                # assume bytes
                pdf_bytes = raw

            return io.BytesIO(pdf_bytes)

        # Download Original Output
        st.download_button(
            label="💾 Download Original Text (TXT)",
            data=st.session_state["recognized_text"].encode("utf-8"),
            file_name="extracted_text.txt",
            mime="text/plain",
            key="download_txt_original"
        )

        pdf_buffer = create_pdf(st.session_state["recognized_text"], "Extracted Text")
        st.download_button(
            label="📄 Download Original Text (PDF)",
            data=pdf_buffer,
            file_name="extracted_text.pdf",
            mime="application/pdf",
            key="download_pdf_original"
        )

        # Translation Section
        st.markdown("### 🌐 Translate and Download")
        languages = {
            "Kannada": "kn",
            "Hindi": "hi",
            "Tamil": "ta",
            "Telugu": "te",
            "Malayalam": "ml",
            "French": "fr",
            "Spanish": "es",
            "German": "de",
            "Italian": "it",
            "Russian": "ru",
            "Japanese": "ja",   
            "Chinese (Simplified)": "zh-cn",
            "Arabic": "ar", 
            "Portuguese": "pt",
            "Bengali": "bn",
            "Urdu": "ur",
            "Korean": "ko",
            "Vietnamese": "vi",
            
        }
        selected_lang = st.selectbox("Select Target Language", list(languages.keys()))
        translator = Translator()

        if st.button("Translate", key=f"translate_{selected_lang}"):
            with st.spinner("Translating..."):
                st.session_state["translated_text"] = translator.translate(
                    st.session_state["recognized_text"],
                    dest=languages[selected_lang]
                ).text
                st.success(f"Translated to {selected_lang}!")

        if st.session_state["translated_text"]:
            translated = st.session_state["translated_text"]
            st.text_area("Translated Output", translated, height=200)

            st.download_button(
                label=f"💾 Download in {selected_lang} (TXT)",
                data=translated.encode("utf-8"),
                file_name=f"extracted_text_{languages[selected_lang]}.txt",
                mime="text/plain",
                key=f"download_txt_{selected_lang}"
            )

    # Footer
    st.markdown("---")
    st.caption("© 2026 CraftIQ — Ns Akash (@craftiq). All rights reserved.")
           

if __name__ == "__main__":
    main(DET_ARCHS, RECO_ARCHS)
