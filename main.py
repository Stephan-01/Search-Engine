
from indexer import index_documents
from gui import create_gui


pdf_folder_path = "Datenbasis"
index = index_documents(pdf_folder_path)


create_gui(index)
