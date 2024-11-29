import os
import shutil
import pyterrier as pt
import pandas as pd
from pdf_utils import extract_text_from_pdf
from search_utils import escape_special_characters
def prepare_corpus(pdf_folder):
    """Erstellt ein Pandas-DataFrame mit den Texten und Metadaten der PDFs."""
    corpus = []
    for file in os.listdir(pdf_folder):
        if file.endswith('.pdf'):
            file_path = os.path.join(pdf_folder, file)
            text = extract_text_from_pdf(file_path)
            corpus.append({"docno": file, "text": text})
    return pd.DataFrame(corpus)

def index_documents(pdf_folder):
    """Indexiert die Dokumente und gibt den Index zurück."""

    index_path = os.path.join(os.getcwd(), "pdf_index")

    # Sicherstellen, dass der Index-Ordner existiert
    if os.path.exists(index_path):
        print(f"Index existiert bereits, der Ordner wird gelöscht: {index_path}")
        shutil.rmtree(index_path)  # Löscht den bestehenden Index-Ordner

    os.makedirs(index_path)  # Erstelle den Ordner für den neuen Index
    print(f"Das Verzeichnis {index_path} wurde erstellt.")

    # Corpus vorbereiten und Index erstellen
    corpus_df = prepare_corpus(pdf_folder)
    indexer = pt.terrier.IterDictIndexer(index_path)
    index_ref = indexer.index(corpus_df.to_dict("records"))
    return pt.IndexFactory.of(index_ref)

def search_query(index, query):
    """Sucht die besten Dokumente für die Anfrage."""
    query = escape_special_characters(query)
    print("Bereinigte Anfrage:", query)
    retriever = pt.terrier.Retriever(index, wmodel="BM25")
    results = retriever.search(query)
    return results.head(3)
