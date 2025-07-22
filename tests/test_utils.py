

from app.services.pdf_utils import extract_text_from_pdf
from app.services.text_utils import (
    chunk_text,
    expand_query_with_synonyms,
    find_best_chunk,
)


def test_chunk_text_basico():
    texto = "a" * 3500
    chunks = chunk_text(texto, chunk_size=1000, overlap=200)
    assert len(chunks) > 1
    assert all(isinstance(chunk, str) for chunk in chunks)
    assert sum(len(chunk) for chunk in chunks) >= len(texto)


def test_expand_query_with_synonyms():
    pergunta = "Como é feita a dispensação de medicamento ao paciente?"
    expandida = expand_query_with_synonyms(pergunta)
    assert "entrega" in expandida or "fornecimento" in expandida
    assert "remédio" in expandida or "fármaco" in expandida
    assert "usuário" in expandida or "cliente" in expandida


def test_find_best_chunk():
    question = "Como é feita a dispensação de medicamento?"
    chunks = [
        "A dispensação de medicamento é realizada por um farmacêutico.",
        "O paciente deve apresentar receita médica.",
        "O fornecimento de remédio segue normas específicas.",
    ]
    best = find_best_chunk(question, chunks)
    assert best in chunks


def test_extract_text_from_pdf(tmp_path):
    # Cria um PDF simples para teste
    from PyPDF2 import PdfWriter

    pdf_path = tmp_path / "teste.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    with open(pdf_path, "wb") as f:
        writer.write(f)
    texto_extraido = extract_text_from_pdf(str(pdf_path))
    assert isinstance(texto_extraido, str)
    # Como a página é em branco, o texto deve ser vazio ou conter mensagem de erro
    assert texto_extraido == "" or "Erro" in texto_extraido
