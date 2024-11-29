import tkinter as tk
from indexer import search_query  # Importiere die Suchfunktion
from search_utils import escape_special_characters
def on_search_click(search_entry, result_list, index):
    """Event-Handler für den Suchbutton."""
    query = search_entry.get()  # Zugriff auf das Eingabefeld

    if not query:
        result_list.delete(0, tk.END)
        result_list.insert(tk.END, "Bitte eine Anfrage eingeben!")
        return

    # Escape von Sonderzeichen, aber ohne das Fragezeichen zu verändern
    query = escape_special_characters(query)

    try:
        # Suche durchführen
        results = search_query(index, query)
        result_list.delete(0, tk.END)

        # Ergebnisse in die GUI einfügen
        for i, row in results.iterrows():
            result_list.insert(tk.END, f"Rank {i+1}: {row['docno']} (Score: {row['score']:.2f})")
    except Exception as e:
        # Fehlerausgabe, wenn etwas schief geht
        result_list.delete(0, tk.END)
        result_list.insert(tk.END, f"Fehler bei der Suche: {str(e)}")

def create_gui(index):
    """Erstellt das GUI und gibt die benötigten Widgets zurück."""
    root = tk.Tk()
    root.title("PDF Suchmaschine")

    # Setze die Hintergrundfarbe des Fensters
    root.configure(bg="#f0f0f0")  # Hellgrau als Hintergrundfarbe

    # Layout
    frame = tk.Frame(root, bg="#d3e0e9")  # Heller Blauton für das Frame
    frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Suchfeld und Button
    search_label = tk.Label(frame, text="Suchanfrage:", bg="#d3e0e9", fg="black", font=("Helvetica", 10, "bold"))
    search_label.grid(row=0, column=0, sticky="w", pady=5)
    search_entry = tk.Entry(frame, width=50, bg="white", fg="black", font=("Helvetica", 10))
    search_entry.grid(row=0, column=1, pady=5, padx=5)

    #Button
    search_button = tk.Button(frame, text="Suchen", command=lambda: on_search_click(search_entry, result_list, index),
                              bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"))
    search_button.grid(row=0, column=2, pady=5, padx=5)

    # Ergebnisanzeige
    result_label = tk.Label(frame, text="Ergebnisse:", bg="#d3e0e9", fg="black", font=("Helvetica", 10, "bold"))
    result_label.grid(row=1, column=0, sticky="nw", pady=5)
    result_list = tk.Listbox(frame, width=80, height=10, bg="white", fg="black", font=("Helvetica", 10))
    result_list.grid(row=1, column=1, columnspan=2, pady=5)

    # GUI starten
    root.mainloop()

    return search_entry, result_list  # Die Widgets werden zurückgegeben
