import tkinter as tk
from indexer import search_query
from search_utils import escape_special_characters
def on_search_click(search_entry, result_list, index):
    """Event-Handler für den Suchbutton."""
    query = search_entry.get()

    if not query:
        result_list.delete(0, tk.END)
        result_list.insert(tk.END, "Bitte eine Anfrage eingeben!")
        return


    query = escape_special_characters(query)

    try:

        results = search_query(index, query)
        result_list.delete(0, tk.END)


        for i, row in results.iterrows():
            result_list.insert(tk.END, f"Rank {i+1}: {row['docno']} (Score: {row['score']:.2f})")
    except Exception as e:

        result_list.delete(0, tk.END)
        result_list.insert(tk.END, f"Fehler bei der Suche: {str(e)}")

def create_gui(index):
    """Erstellt das GUI und gibt die benötigten Widgets zurück."""
    root = tk.Tk()
    root.title("PDF Suchmaschine")


    root.configure(bg="#f0f0f0")

    # Layout
    frame = tk.Frame(root, bg="#d3e0e9")
    frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)


    search_label = tk.Label(frame, text="Suchanfrage:", bg="#d3e0e9", fg="black", font=("Helvetica", 10, "bold"))
    search_label.grid(row=0, column=0, sticky="w", pady=5)
    search_entry = tk.Entry(frame, width=50, bg="white", fg="black", font=("Helvetica", 10))
    search_entry.grid(row=0, column=1, pady=5, padx=5)


    search_button = tk.Button(frame, text="Suchen", command=lambda: on_search_click(search_entry, result_list, index),
                              bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"))
    search_button.grid(row=0, column=2, pady=5, padx=5)


    result_label = tk.Label(frame, text="Ergebnisse:", bg="#d3e0e9", fg="black", font=("Helvetica", 10, "bold"))
    result_label.grid(row=1, column=0, sticky="nw", pady=5)
    result_list = tk.Listbox(frame, width=80, height=10, bg="white", fg="black", font=("Helvetica", 10))
    result_list.grid(row=1, column=1, columnspan=2, pady=5)


    root.mainloop()

    return search_entry, result_list
