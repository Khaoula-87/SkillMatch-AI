
import re
from src.preprocessing import normalize_text


SKILLS = {
    "Python": ["python"],
    "SQL": ["sql"],
    "Java": ["java"],
    "R": ["r language", "langage r"],

    "Machine Learning": [
        "machine learning",
        "apprentissage automatique",
        "ml"
    ],

    "Deep Learning": [
        "deep learning",
        "apprentissage profond",
        "dl"
    ],

    "NLP": [
        "nlp",
        "natural language processing",
        "traitement automatique du langage",
        "traitement du langage naturel",
        "tal"
    ],

    "Computer Vision": [
        "computer vision",
        "vision par ordinateur"
    ],

    "LLM": [
        "llm",
        "large language model",
        "large language models",
        "grands modeles de langage"
    ],

    "Generative AI": [
        "generative ai",
        "ia generative",
        "genai"
    ],

    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "PyTorch": ["pytorch"],
    "TensorFlow": ["tensorflow"],
    "Hugging Face": ["hugging face", "huggingface"],

    "Spark": ["apache spark", "pyspark", "spark"],
    "Hadoop": ["hadoop"],
    "Kafka": ["apache kafka", "kafka"],
    "Elasticsearch": ["elasticsearch"],
    "Kibana": ["kibana"],
    "Logstash": ["logstash"],

    "Docker": ["docker"],
    "Git": ["git"],
    "FastAPI": ["fastapi"],
    "Streamlit": ["streamlit"],

    "Power BI": ["power bi", "powerbi"],
    "Tableau": ["tableau software", "tableau desktop"],

    "ETL": ["etl", "extract transform load"],
    "Big Data": ["big data"],
    "Data Science": ["data science", "science des donnees"],
    "Data Engineering": [
        "data engineering",
        "ingenierie des donnees"
    ]
}


def extract_skills(text):
    """Extraire les compétences et normaliser leurs noms."""

    text = normalize_text(text)
    detected = set()

    for skill, aliases in SKILLS.items():
        for alias in aliases:
            alias = normalize_text(alias)

            pattern = (
                r"(?<!\w)" +
                re.escape(alias) +
                r"(?!\w)"
            )

            if re.search(pattern, text):
                detected.add(skill)
                break

    return sorted(detected)
