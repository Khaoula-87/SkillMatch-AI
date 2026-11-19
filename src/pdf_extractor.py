
import fitz


def extract_pdf_text(uploaded_file):
    """Extraire le texte d'un PDF chargé dans Streamlit."""

    pdf_bytes = uploaded_file.getvalue()
    text = []

    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page in doc:
            text.append(page.get_text())

    return "\n".join(text)
