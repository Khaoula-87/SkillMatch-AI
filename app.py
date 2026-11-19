
from pathlib import Path
import hashlib

import pandas as pd
import streamlit as st

from src.pdf_extractor import extract_pdf_text
from src.skill_extractor import extract_skills
from src.matching import rank_offers


ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "offres.csv"
EVAL_PATH = ROOT / "results" / "comparaison_modeles.csv"

st.set_page_config(
    page_title="SkillMatch | Analyse de CV",
    page_icon="📄",
    layout="wide"
)


# ------------------------------------------
# STYLE
# ------------------------------------------

st.markdown("""
<style>
.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    letter-spacing: -0.025em;
}

div[data-testid="stMetric"] {
    border: 1px solid rgba(128,128,128,0.25);
    border-radius: 10px;
    padding: 15px;
}

div[data-testid="stFileUploader"] {
    border-radius: 10px;
}

.stButton > button {
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)


# ------------------------------------------
# FONCTIONS
# ------------------------------------------

def normalize_skills(value):
    """Convertit les compétences en liste."""
    if isinstance(value, (list, tuple, set)):
        return [str(x) for x in value]

    if value is None:
        return []

    if isinstance(value, str):
        if not value.strip():
            return []
        return [
            x.strip()
            for x in value.split(",")
            if x.strip()
        ]

    return []


def display_skills(skills, empty_message):
    skills = normalize_skills(skills)

    if skills:
        st.write(" · ".join(skills))
    else:
        st.caption(empty_message)


def export_ranking(results):
    exported = results.copy()

    for col in [
        "competences_communes",
        "competences_manquantes"
    ]:
        if col in exported.columns:
            exported[col] = exported[col].apply(
                lambda x: ", ".join(normalize_skills(x))
            )

    return exported.to_csv(
        index=False
    ).encode("utf-8-sig")


def display_offer(row, position):
    score = float(row["score"])

    with st.container(border=True):
        st.markdown(
            f"#### {position:02d} — {row['titre']}"
        )

        c1, c2 = st.columns([1, 3])

        with c1:
            st.metric(
                "Similarité",
                f"{score:.3f}"
            )

        with c2:
            st.write("**Description du poste**")
            st.write(row["description"])

        st.write("**Compétences correspondantes**")
        display_skills(
            row["competences_communes"],
            "Aucune correspondance détectée."
        )

        st.write("**Compétences non détectées dans le CV**")
        display_skills(
            row["competences_manquantes"],
            "Aucune compétence manquante détectée."
        )


def get_ranking(cv_text, offers, method):
    results = rank_offers(
        cv_text,
        offers,
        method=method
    )

    if results["score"].isna().any():
        raise ValueError(
            f"Scores invalides pour {method}."
        )

    return results


# ------------------------------------------
# DONNÉES
# ------------------------------------------

if not DATA_PATH.exists():
    st.error("Le fichier data/offres.csv est introuvable.")
    st.stop()

offers = pd.read_csv(
    DATA_PATH,
    dtype={"id": str}
).fillna("")

required = {
    "id", "titre", "description", "competences"
}

missing = required - set(offers.columns)

if missing:
    st.error(
        "Colonnes manquantes : " + ", ".join(sorted(missing))
    )
    st.stop()

if offers.empty:
    st.warning("Le dataset ne contient aucune offre.")
    st.stop()


# ------------------------------------------
# EN-TÊTE
# ------------------------------------------

st.title("SkillMatch")
st.caption(
    "Analyse de CV et recommandation d'offres de stage"
)

st.divider()

tab_cv, tab_compare, tab_eval = st.tabs([
    "Analyse CV",
    "Comparaison des modèles",
    "Évaluation"
])


# ==========================================
# ONGLET 1 : ANALYSE CV
# ==========================================

with tab_cv:

    st.subheader("Importer un CV")

    cv = st.file_uploader(
        "Sélectionner un document PDF",
        type=["pdf"],
        key="cv_upload"
    )

    st.caption(
        f"Catalogue actuel : {len(offers)} offres de stage."
    )

    with st.expander("Consulter le catalogue"):
        st.dataframe(
            offers,
            use_container_width=True,
            hide_index=True
        )

    if cv is not None:

        cv_hash = hashlib.sha256(
            cv.getvalue()
        ).hexdigest()

        try:
            cv_text = extract_pdf_text(cv)
        except Exception as exc:
            st.error(f"Lecture impossible : {exc}")
            st.stop()

        if not cv_text.strip():
            st.warning(
                "Ce PDF ne contient pas de texte extractible."
            )
            st.stop()

        skills = normalize_skills(
            extract_skills(cv_text)
        )

        st.divider()
        st.subheader("Profil extrait")

        col1, col2, col3 = st.columns(3)

        col1.metric("Document", "PDF")
        col2.metric("Compétences détectées", len(skills))
        col3.metric("Offres disponibles", len(offers))

        with st.expander("Consulter le texte extrait"):
            st.text_area(
                "Contenu du document",
                cv_text[:10000],
                height=220,
                disabled=True
            )

        st.write("**Compétences identifiées**")
        display_skills(
            skills,
            "Aucune compétence reconnue dans le dictionnaire."
        )

        st.divider()
        st.subheader("Recommandations")

        col_method, col_k = st.columns(2)

        with col_method:
            method = st.selectbox(
                "Méthode de classement",
                ["Sentence-BERT", "TF-IDF"]
            )

        with col_k:
            top_k = st.slider(
                "Nombre de recommandations",
                min_value=1,
                max_value=min(10, len(offers)),
                value=min(5, len(offers))
            )

        if st.button(
            "Analyser les correspondances",
            type="primary"
        ):
            with st.spinner("Calcul du classement..."):
                try:
                    ranking = get_ranking(
                        cv_text,
                        offers,
                        method
                    )

                    st.session_state["ranking"] = ranking
                    st.session_state["ranking_method"] = method
                    st.session_state["ranking_cv_hash"] = cv_hash

                except Exception as exc:
                    st.error(f"Erreur : {exc}")

        valid_ranking = (
            "ranking" in st.session_state
            and st.session_state.get(
                "ranking_method"
            ) == method
            and st.session_state.get(
                "ranking_cv_hash"
            ) == cv_hash
        )

        if valid_ranking:

            ranking = st.session_state["ranking"]
            top = ranking.head(top_k)

            st.divider()
            st.subheader(
                f"Les {top_k} meilleures correspondances"
            )

            st.caption(
                "La similarité mesure la proximité des textes. "
                "Elle ne prédit pas les chances de recrutement."
            )

            for position, (_, row) in enumerate(
                top.iterrows(), start=1
            ):
                display_offer(row, position)

            st.subheader("Répartition des scores")

            chart = top[
                ["id", "titre", "score"]
            ].copy()

            chart["offre"] = (
                chart["id"].astype(str)
                + " — "
                + chart["titre"].astype(str)
            )

            st.bar_chart(
                chart.set_index("offre")[["score"]],
                horizontal=True
            )

            st.download_button(
                "Exporter le classement CSV",
                data=export_ranking(ranking),
                file_name="skillmatch_classement.csv",
                mime="text/csv"
            )

    else:
        st.info(
            "Importez un CV pour afficher son profil "
            "et rechercher les offres correspondantes."
        )


# ==========================================
# ONGLET 2 : COMPARAISON DES MODÈLES
# ==========================================

with tab_compare:

    st.subheader("Comparaison sur un même CV")

    st.write(
        "Les deux méthodes analysent le même document "
        "et le même catalogue d'offres."
    )

    if cv is None:
        st.info(
            "Importez d'abord un CV dans l'onglet Analyse CV."
        )

    else:
        if st.button(
            "Comparer TF-IDF et Sentence-BERT",
            type="primary"
        ):

            with st.spinner(
                "Calcul des deux classements..."
            ):
                try:
                    tfidf = get_ranking(
                        cv_text,
                        offers,
                        "TF-IDF"
                    )

                    sbert = get_ranking(
                        cv_text,
                        offers,
                        "Sentence-BERT"
                    )

                    st.session_state["comparison"] = {
                        "TF-IDF": tfidf,
                        "Sentence-BERT": sbert
                    }

                    st.session_state[
                        "comparison_cv_hash"
                    ] = cv_hash

                except Exception as exc:
                    st.error(f"Erreur : {exc}")

        valid_comparison = (
            "comparison" in st.session_state
            and st.session_state.get(
                "comparison_cv_hash"
            ) == cv_hash
        )

        if valid_comparison:

            comparison = st.session_state["comparison"]

            left, right = st.columns(2)

            for column, model in [
                (left, "TF-IDF"),
                (right, "Sentence-BERT")
            ]:

                with column:
                    st.markdown(f"### {model}")

                    top = comparison[model].head(5)

                    for position, (_, row) in enumerate(
                        top.iterrows(), start=1
                    ):
                        with st.container(border=True):
                            st.write(
                                f"**{position}. {row['titre']}**"
                            )
                            st.metric(
                                "Similarité",
                                f"{float(row['score']):.3f}"
                            )
                            st.caption(
                                f"Référence : {row['id']}"
                            )

            st.divider()
            st.subheader("Différences entre les classements")

            a = comparison["TF-IDF"].head(5)
            b = comparison["Sentence-BERT"].head(5)

            common_ids = (
                set(a["id"].astype(str))
                & set(b["id"].astype(str))
            )

            st.metric(
                "Offres communes dans les deux Top 5",
                f"{len(common_ids)}/5"
            )

            st.caption(
                "Les scores des deux modèles ne sont "
                "pas nécessairement calibrés de la même façon."
            )


# ==========================================
# ONGLET 3 : ÉVALUATION
# ==========================================

with tab_eval:

    st.subheader("Résultats expérimentaux")

    if EVAL_PATH.exists():

        evaluation = pd.read_csv(EVAL_PATH)

        metrics = [
            "Precision@5",
            "Recall@5",
            "nDCG@5"
        ]

        expected = {"modele", *metrics}

        if not expected.issubset(evaluation.columns):
            st.error(
                "Le fichier d'évaluation ne possède "
                "pas les colonnes attendues."
            )

        else:
            summary = (
                evaluation.groupby("modele")[metrics]
                .mean()
                .round(4)
            )

            st.write("**Performances moyennes**")

            st.dataframe(
                summary,
                use_container_width=True
            )

            st.write("**Comparaison graphique**")

            st.bar_chart(summary)

            with st.expander(
                "Consulter les résultats détaillés"
            ):
                st.dataframe(
                    evaluation,
                    use_container_width=True,
                    hide_index=True
                )

            st.download_button(
                "Exporter les métriques",
                data=evaluation.to_csv(
                    index=False
                ).encode("utf-8-sig"),
                file_name="skillmatch_evaluation.csv",
                mime="text/csv"
            )

            st.caption(
                "Évaluation exploratoire sur des offres "
                "synthétiques annotées par IA. "
                "Ces résultats ne constituent pas "
                "une validation humaine indépendante."
            )

    else:
        st.info(
            "Exécutez python evaluate_models.py "
            "pour générer les métriques."
        )


# ------------------------------------------
# PIED DE PAGE
# ------------------------------------------

st.divider()

st.caption(
    "SkillMatch | Projet académique NLP "
    "| TF-IDF et Sentence-BERT"
)
