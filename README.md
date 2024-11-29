
markdown
Code kopieren
# PDF Suchmaschine

Dieses Projekt bietet eine grafische Benutzeroberfläche (GUI) zur Durchsuchung von PDF-Dokumenten. Die Anwendung nutzt moderne Tools wie **PyTerrier**, **spaCy** und **PyPDF2**, um eine effiziente Suche zu ermöglichen.

## Funktionen

- **PDF-Text-Extraktion**  
  Text wird aus PDF-Dokumenten extrahiert und zur Indexierung aufbereitet.

- **Indexierung**  
  Die PDFs werden mit PyTerrier in einem BM25-Index gespeichert.

- **Schnelle Suche**  
  Benutzer können eine Sucheingabe in der GUI machen, und die besten Ergebnisse werden aufgelistet.

- **Suchoptimierung:**  
  Bereinigt die Suchanfragen von Stoppwörtern und Sonderzeichen. (unter Verwendung von spaCy).

- **Benutzerfreundliche Oberfläche**  
  Die intuitive GUI ermöglicht eine einfache Nutzung.

![GUI](fig1.PNG)
