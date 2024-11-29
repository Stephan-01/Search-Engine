import re
import spacy


nlp = spacy.load("de_core_news_sm")  # Für Deutsch, für Englisch "en_core_web_sm"

def escape_special_characters(query):
    """Entfernt alle Sonderzeichen und Stoppwörter aus der Anfrage, behält aber normale Buchstaben und Zahlen bei."""

    # Verarbeite die Anfrage mit spaCy, um Stoppwörter zu erkennen
    doc = nlp(query)

    # Filtere Stoppwörter und nicht-alphabetische Zeichen heraus
    filtered_query = ' '.join([token.text for token in doc if not token.is_stop and token.is_alpha])


    return filtered_query