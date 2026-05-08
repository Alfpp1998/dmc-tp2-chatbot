"""
Búsqueda Vectorial con PDFs - Vector Store Local (JSON)
Extrae texto de PDFs en la carpeta pdfs/, genera embeddings y permite búsquedas.
"""
import os
import re
from typing import List, Dict

from pypdf import PdfReader

from vector_search_local import LocalEmbeddings, JSONVectorStore, Config
import warnings
warnings.filterwarnings('ignore')


def clean_text(text: str) -> str:
    """Limpia texto extraído de PDFs"""
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r' {2,}', ' ', text)
    text = text.replace("  ", " ")
    text = text.replace("...", "")
    text = text.replace(" - ", "")
    text = text.replace(" - ", "")
    return text.strip()


def extract_pdf_text(pdf_path: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[str]:
    """Extrae texto de un PDF y lo divide en chunks"""
    reader = PdfReader(pdf_path)
    full_text = ""
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            full_text += text + "\n"

    full_text = clean_text(full_text)

    # Dividir en chunks con overlap
    paragraphs = full_text.split('\n')
    chunks = []
    current = ""

    for para in paragraphs:
        if len(current) + len(para) < chunk_size:
            current += para + " "
        else:
            if current.strip():
                chunks.append(current.strip())
            current = para + " "

            # Solapamiento: mantener últimas palabras del chunk anterior
            if over := min(chunk_overlap, len(current)):
                pass  # Ya incluido en el slice del chunk anterior

    if current.strip():
        chunks.append(current.strip())

    return chunks


def process_all_pdfs(pdf_folder: str = "pdfs", store_path: str = "pdf_vector_store.json") -> JSONVectorStore:
    """Procesa todos los PDFs de la carpeta y los indexa"""
    store = JSONVectorStore(store_path)

    if not os.path.exists(pdf_folder):
        print(f"Carpeta {pdf_folder} no encontrada")
        return store

    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith('.pdf')]
    print(f"Encontrados {len(pdf_files)} PDFs: {pdf_files}")

    all_texts = []
    all_metadatas = []

    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_folder, pdf_file)
        print(f"\nProcesando: {pdf_file} ...")
        chunks = extract_pdf_text(pdf_path)
        print(f"  Extraídos {len(chunks)} chunks de texto")

        for i, chunk in enumerate(chunks):
            all_texts.append(chunk)
            all_metadatas.append({
                "pdf_name": pdf_file,
                "chunk_id": i,
                "source": pdf_path
            })

    # Indexar todos los textos
    if all_texts:
        count = store.add_texts(all_texts, all_metadatas)
        print(f"\n✓ Total indexado: {count} chunks de {len(pdf_files)} PDFs")
    else:
        print("No se extrajo texto de los PDFs")

    return store


def main():
    """Demo con PDFs reales"""
    print("=" * 70)
    print("MOTOR DE BÚSQUEDA VECTORIAL - PDFs con JSON Local")
    print("=" * 70 + "\n")

    Config.print_config()

    # Procesar PDFs e indexar
    store = process_all_pdfs()

    if not store.store:
        print("No hay documentos indexados. Saliendo.")
        return

    # Búsquedas de prueba
    queries = [
        "¿Cuáles son los productos del catálogo?",
        "cual fué el presidente que firmó la constitución?",
        "¿Qué dice sobre ciencia y tecnología?"
    ]

    for query in queries:
        print(f"\n{'=' * 70}")
        print(f"Query: {query}")
        print("=" * 70)

        results = store.search(query, k=5)
        for j, r in enumerate(results, 1):
            # Mostrar solo primeras 200 caracteres del texto
            text_preview = r['text'][:200].replace('\n', ' ')
            print(f"\n{j}. [Score: {r['score']:.4f}]")
            print(f"   PDF: {r['metadata'].get('pdf_name', 'N/A')}")
            print(f"   Texto: {text_preview}...")

    # Estadísticas finales
    print(f"\n{'=' * 70}")
    print("ESTADÍSTICAS")
    print("=" * 70)
    for k, v in store.stats().items():
        print(f"{k}: {v}")

    print("\n¡Demo completada!")


if __name__ == "__main__":
    main()