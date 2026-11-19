
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def tfidf_matching(cv_text, offers_texts):
    """
    Calculer la similarité TF-IDF entre
    un CV et plusieurs offres de stage.
    """

    documents = [cv_text] + list(offers_texts)

    vectorizer = TfidfVectorizer(
        lowercase=True,
        strip_accents="unicode",
        stop_words=None,
        ngram_range=(1, 2)
    )

    matrix = vectorizer.fit_transform(documents)

    cv_vector = matrix[0:1]
    offers_vectors = matrix[1:]

    scores = cosine_similarity(
        cv_vector,
        offers_vectors
    )[0]

    return scores
