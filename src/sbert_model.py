
import numpy as np
import streamlit as st

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


@st.cache_resource
def load_sbert_model():
    return SentenceTransformer(
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        device="cpu"
    )



def sbert_matching(cv_text, offers_texts):
    import numpy as np

    model = load_sbert_model()

    texts = [str(cv_text)] + [
        str(text) for text in offers_texts
    ]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False
    )

    # Utiliser float64 pour améliorer
    # la stabilité numérique
    embeddings = np.asarray(
        embeddings, dtype=np.float64
    )

    if not np.isfinite(embeddings).all():
        raise ValueError("Embeddings SBERT invalides")

    cv_embedding = embeddings[0]
    offer_embeddings = embeddings[1:]

    # Calcul des similarités sans matmul
    scores = np.array([
        np.sum(offer * cv_embedding)
        for offer in offer_embeddings
    ])

    if not np.isfinite(scores).all():
        raise ValueError("Scores SBERT invalides")

    return scores

