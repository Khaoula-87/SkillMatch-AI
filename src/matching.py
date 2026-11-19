
import pandas as pd

from src.skill_extractor import extract_skills
from src.tfidf_model import tfidf_matching
from src.sbert_model import sbert_matching


def prepare_offer_text(row):
    """Construire le texte utilisé pour le matching."""

    title = str(row.get("titre", "") or "")
    description = str(row.get("description", "") or "")
    skills = str(row.get("competences", "") or "")

    return f"{title}. {description}. {skills}"


def rank_offers(cv_text, offers_df, method="TF-IDF"):
    """
    Classer les offres selon leur similarité
    avec le CV.
    """

    df = offers_df.copy().fillna("")

    offer_texts = [
        prepare_offer_text(row)
        for _, row in df.iterrows()
    ]

    if method == "TF-IDF":
        scores = tfidf_matching(cv_text, offer_texts)

    elif method == "Sentence-BERT":
        scores = sbert_matching(cv_text, offer_texts)

    else:
        raise ValueError("Méthode inconnue")

    df["score"] = scores

    cv_skills = set(extract_skills(cv_text))

    common_skills = []
    missing_skills = []

    for _, row in df.iterrows():

        offer_skills = set(
            extract_skills(
                str(row.get("competences", ""))
            )
        )

        common = sorted(cv_skills & offer_skills)
        missing = sorted(offer_skills - cv_skills)

        common_skills.append(common)
        missing_skills.append(missing)

    df["competences_communes"] = common_skills
    df["competences_manquantes"] = missing_skills

    df = df.sort_values(
        by="score",
        ascending=False
    ).reset_index(drop=True)

    return df
