
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent

annotations_path = ROOT / "data" / "annotations.csv"
offers_path = ROOT / "data" / "offres.csv"
cv_dir = ROOT / "data" / "cvs"

st.set_page_config(
    page_title="Annotation SkillMatch AI",
    page_icon="📝",
    layout="wide"
)

st.title("📝 Annotation des offres de stage")

annotations = pd.read_csv(
    annotations_path,
    dtype={"cv_id": str, "offre_id": str}
)

offers = pd.read_csv(
    offers_path,
    dtype={"id": str}
).fillna("")

cv_ids = annotations["cv_id"].unique().tolist()

selected_cv = st.selectbox(
    "Sélectionner un CV",
    cv_ids
)

cv_path = cv_dir / f"{selected_cv}.txt"

if cv_path.exists():
    with st.expander("📄 Contenu du CV", expanded=True):
        st.text(
            cv_path.read_text(encoding="utf-8")
        )
else:
    st.warning(f"CV introuvable : {cv_path.name}")

subset = annotations[
    annotations["cv_id"] == selected_cv
]

completed = subset["pertinence"].notna().sum()

st.progress(completed / len(subset))

st.write(
    f"**Progression : {completed}/{len(subset)} "
    "offres annotées**"
)

for idx, row in subset.iterrows():

    offer = offers[
        offers["id"] == row["offre_id"]
    ]

    if offer.empty:
        continue

    offer = offer.iloc[0]

    with st.expander(
        f"{row['offre_id']} — {offer['titre']}"
    ):

        st.write(
            "**Description :**",
            offer.get("description", "")
        )

        st.write(
            "**Compétences recherchées :**",
            offer.get("competences", "")
        )

        current = row["pertinence"]

        options = ["Non annotée", 0, 1, 2]

        current_value = (
            "Non annotée"
            if pd.isna(current)
            else int(current)
        )

        value = st.selectbox(
            "Note de pertinence",
            options,
            index=options.index(current_value),
            key=f"note_{selected_cv}_{idx}"
        )

        if st.button(
            "💾 Enregistrer",
            key=f"save_{selected_cv}_{idx}"
        ):

            annotations.loc[idx, "pertinence"] = (
                None if value == "Non annotée"
                else value
            )

            annotations.to_csv(
                annotations_path,
                index=False,
                encoding="utf-8-sig"
            )

            st.success("Annotation enregistrée")
            st.rerun()
