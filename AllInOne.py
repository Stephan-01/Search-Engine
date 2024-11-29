import os
import pyterrier as pt
import PyPDF2
import pandas as pd
import tkinter as tk
import shutil
from tkinter import ttk

# PyTerrier initialisieren
if not pt.java.started():
    pt.java.init()

def extract_text_from_pdf(file_path):
    """Extrahiert Text aus einer PDF-Datei."""
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

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
    # Pfad zum Index-Verzeichnis (absolut)
    index_path = os.path.join(os.getcwd(), "pdf_index")

    # Sicherstellen, dass der Index-Ordner existiert
    if os.path.exists(index_path):
        print(f"Index existiert bereits, der Ordner wird gelöscht: {index_path}")
        shutil.rmtree(index_path)  # Löscht den bestehenden Index-Ordner

    os.makedirs(index_path)  # Erstelle den Ordner für den neuen Index
    print(f"Das Verzeichnis {index_path} wurde erstellt.")

    # Corpus vorbereiten und Index erstellen
    corpus_df = prepare_corpus(pdf_folder)
    indexer = pt.IterDictIndexer(index_path)
    index_ref = indexer.index(corpus_df.to_dict("records"))
    return pt.IndexFactory.of(index_ref)
def search_query(index, query):
    """Sucht die besten Dokumente für die Anfrage."""
    # Verwenden des Retrievers und festlegen des BM25-Modells
    retriever = pt.terrier.Retriever(index, wmodel="BM25")
    results = retriever.search(query)
    return results.head(3)


def on_search_click():
    """Event-Handler für den Suchbutton."""
    query = search_entry.get()
    if not query:
        result_list.delete(0, tk.END)
        result_list.insert(tk.END, "Bitte eine Anfrage eingeben!")
        return

    results = search_query(index, query)
    result_list.delete(0, tk.END)
    for i, row in results.iterrows():
        result_list.insert(tk.END, f"Rank {i+1}: {row['docno']} (Score: {row['score']:.2f})")

# Ordner mit PDFs festlegen
pdf_folder_path = "Datenbasis"  # Ordner mit PDFs
index = index_documents(pdf_folder_path)  # Index erstellen

# GUI erstellen
root = tk.Tk()
root.title("PDF Suchmaschine")

# Layout
frame = tk.Frame(root)
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Suchfeld und Button
search_label = tk.Label(frame, text="Suchanfrage:")
search_label.grid(row=0, column=0, sticky="w", pady=5)
search_entry = tk.Entry(frame, width=50)
search_entry.grid(row=0, column=1, pady=5, padx=5)
search_button = tk.Button(frame, text="Suchen", command=on_search_click)
search_button.grid(row=0, column=2, pady=5, padx=5)

# Ergebnisanzeige
result_label = tk.Label(frame, text="Ergebnisse:")
result_label.grid(row=1, column=0, sticky="nw", pady=5)
result_list = tk.Listbox(frame, width=80, height=10)
result_list.grid(row=1, column=1, columnspan=2, pady=5)

# GUI starten
root.mainloop()
