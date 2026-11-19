
import re
import unicodedata


def normalize_text(text):
    """Normaliser un texte pour faciliter la recherche NLP."""
    if not isinstance(text, str):
        return ""

    text = text.lower()

    # Supprimer les accents
    text = unicodedata.normalize("NFKD", text)
    text = "".join(
        c for c in text
        if not unicodedata.combining(c)
    )

    # Uniformiser les espaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def clean_text(text):
    """Nettoyage léger sans supprimer les termes techniques."""
    text = normalize_text(text)

    # Conserver les caractères utiles : C++, C#, .NET
    text = re.sub(r"[^\w\s+#.\-/]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()
