"""
Funções utilitárias para extração de texto de arquivos PDF.
"""


from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extrai o texto de um arquivo PDF.

    Parâmetros:
        pdf_path (str): Caminho para o arquivo PDF.

    Retorna:
        str: Texto extraído do PDF.
    """
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        text = f"Erro ao extrair texto do PDF: {e}"
    return text
