
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
CV_DIR = ROOT / "data" / "cvs"
OFFERS_PATH = ROOT / "data" / "offres.csv"
OUTPUT = ROOT / "data" / "annotations.csv"

offers = pd.read_csv(OFFERS_PATH).fillna("")
cv_files = sorted(CV_DIR.glob("*.txt"))

if len(cv_files) < 3:
    raise ValueError(
        "Il faut au moins 3 CV TXT dans data/cvs/"
    )

rows = []

for cv_file in cv_files[:3]:
    cv_id = cv_file.stem

    for _, offer in offers.iterrows():
        rows.append({
            "cv_id": cv_id,
            "offre_id": str(offer["id"]),
            "titre": offer["titre"],
            "competences_offre": offer["competences"],
            "pertinence": "",
            "justification": ""
        })

annotations = pd.DataFrame(rows)

if OUTPUT.exists():
    raise FileExistsError(
        "annotations.csv existe déjà. "
        "Ne pas écraser les annotations."
    )

annotations.to_csv(
    OUTPUT,
    index=False,
    encoding="utf-8-sig"
)

print(f"{len(annotations)} paires créées")
print(f"Fichier : {OUTPUT}")
print("Remplir pertinence avec 0, 1 ou 2.")
