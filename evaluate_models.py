
from pathlib import Path
import pandas as pd

from src.matching import rank_offers
from src.evaluation import evaluate_ranking


ROOT = Path(__file__).resolve().parent

offers = pd.read_csv(
    ROOT / "data" / "offres.csv",
    dtype={"id": str}
).fillna("")

annotations = pd.read_csv(
    ROOT / "data" / "annotations.csv",
    dtype={"cv_id": str, "offre_id": str}
)

if annotations["pertinence"].isna().any():
    raise ValueError(
        "Annotations incomplètes : remplir "
        "toutes les notes de pertinence."
    )

annotations["pertinence"] = pd.to_numeric(
    annotations["pertinence"],
    errors="raise"
)

if not annotations["pertinence"].isin([0, 1, 2]).all():
    raise ValueError("Notes autorisées : 0, 1, 2")

if annotations.duplicated(
    ["cv_id", "offre_id"]
).any():
    raise ValueError("Annotations dupliquées")

results = []

for cv_id, group in annotations.groupby("cv_id"):

    cv_path = ROOT / "data" / "cvs" / f"{cv_id}.txt"

    if not cv_path.exists():
        raise FileNotFoundError(cv_path)

    cv_text = cv_path.read_text(
        encoding="utf-8"
    )

    relevance = dict(zip(
        group["offre_id"],
        group["pertinence"].astype(int)
    ))

    for method in ["TF-IDF", "Sentence-BERT"]:

        ranking = rank_offers(
            cv_text,
            offers,
            method=method
        )

        metrics = evaluate_ranking(
            ranking["id"].astype(str).tolist(),
            relevance,
            k=5
        )

        results.append({
            "cv_id": cv_id,
            "modele": method,
            **metrics
        })

        print(cv_id, method, metrics)

results_df = pd.DataFrame(results)

output_dir = ROOT / "results"
output_dir.mkdir(exist_ok=True)

results_df.to_csv(
    output_dir / "comparaison_modeles.csv",
    index=False
)

summary = (
    results_df.groupby("modele")[
        ["Precision@5", "Recall@5", "nDCG@5"]
    ]
    .mean()
    .round(4)
)

summary.to_csv(
    output_dir / "resume_evaluation.csv"
)

print("\n=== COMPARAISON MOYENNE ===")
print(summary)
