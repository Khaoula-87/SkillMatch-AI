
import numpy as np
from sklearn.metrics import ndcg_score


def evaluate_ranking(
    ranked_offer_ids,
    relevance_by_id,
    k=5
):
    """
    Évaluer un classement avec des jugements
    de pertinence complets : 0, 1 ou 2.
    """

    ranked_ids = [str(x) for x in ranked_offer_ids]

    if len(ranked_ids) != len(set(ranked_ids)):
        raise ValueError("Identifiants d'offres dupliqués")

    if set(ranked_ids) != set(relevance_by_id):
        raise ValueError(
            "Toutes les offres classées doivent "
            "posséder une annotation."
        )

    if any(
        value not in (0, 1, 2)
        for value in relevance_by_id.values()
    ):
        raise ValueError("Notes autorisées : 0, 1, 2")

    k = min(k, len(ranked_ids))
    top_ids = ranked_ids[:k]

    # Pertinent = niveau 1 ou 2
    relevant = {
        offer_id
        for offer_id, grade in relevance_by_id.items()
        if grade >= 1
    }

    retrieved = sum(
        offer_id in relevant
        for offer_id in top_ids
    )

    precision = retrieved / k

    recall = (
        retrieved / len(relevant)
        if relevant else 0.0
    )

    # nDCG avec niveaux gradués 0, 1, 2
    true_relevance = np.array([
        relevance_by_id[offer_id]
        for offer_id in ranked_ids
    ], dtype=float)

    # Scores décroissants pour reproduire
    # exactement l'ordre du classement
    ranking_scores = np.arange(
        len(ranked_ids), 0, -1,
        dtype=float
    )

    ndcg = ndcg_score(
        [true_relevance],
        [ranking_scores],
        k=k
    ) if true_relevance.max() > 0 else 0.0

    return {
        "Precision@5": round(precision, 4),
        "Recall@5": round(recall, 4),
        "nDCG@5": round(float(ndcg), 4)
    }
