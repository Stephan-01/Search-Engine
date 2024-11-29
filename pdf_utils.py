import PyPDF2


def extract_text_from_pdf(file_path):
    """Extrahiert Text aus einer PDF-Datei."""
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text
