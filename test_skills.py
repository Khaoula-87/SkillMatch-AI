
from src.skill_extractor import extract_skills

cv = """
Étudiante en Data Science et Big Data.

Compétences :
Python, SQL, Machine Learning,
Deep Learning, traitement du langage naturel,
Apache Spark, Elasticsearch, Docker et FastAPI.

Projets :
Développement d'une application utilisant
Scikit-learn, PyTorch et Hugging Face.
"""

skills = extract_skills(cv)

print("Compétences détectées :")

for skill in skills:
    print("-", skill)

print("Total :", len(skills))
