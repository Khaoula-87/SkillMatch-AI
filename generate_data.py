import csv
from pathlib import Path
root=Path(__file__).resolve().parent
(root/'data'/'cvs').mkdir(parents=True,exist_ok=True)
roles={
'Data Scientist':('Python, Pandas, scikit-learn, SQL, Machine Learning','Analyse de données, préparation des variables et entraînement de modèles prédictifs.'),
'Data Engineer':('Python, SQL, Spark, ETL, Elasticsearch','Construction de pipelines de données et traitement de volumes importants.'),
'NLP Engineer':('Python, NLP, Transformers, PyTorch, Hugging Face','Classification de textes, embeddings et recherche sémantique.'),
'ML Engineer':('Python, Docker, FastAPI, Machine Learning, Git','Déploiement de modèles et création de services de prédiction.'),
'BI Analyst':('SQL, Power BI, Excel, Python','Création de tableaux de bord et analyse des indicateurs métier.'),
'Computer Vision Engineer':('Python, PyTorch, OpenCV, Deep Learning','Analyse d’images et expérimentation de réseaux neuronaux.'),
'Cybersecurity Data Analyst':('Python, Elasticsearch, Kibana, SQL','Analyse de journaux de sécurité et détection de comportements inhabituels.'),
'Cloud Data Engineer':('Python, SQL, Docker, Spark, Cloud','Développement de traitements de données dans un environnement cloud.'),
'AI Research Intern':('Python, PyTorch, Transformers, Deep Learning','Expérimentation, comparaison et évaluation de modèles IA.'),
'Backend Python Developer':('Python, FastAPI, SQL, Docker, Git','Développement d’API et intégration de services de données.')}
rows=[]
for i in range(50):
    title,(skills,desc)=list(roles.items())[i%len(roles)]
    level=['débutant','intermédiaire','avancé'][i%3]
    rows.append({'id':f'OFF-{i+1:03d}','titre':f'Stage {title} — {i//10+1}','description':f'{desc} Stage de niveau {level}. Travail en équipe et documentation des résultats.','competences':skills})
with (root/'data'/'offres.csv').open('w',newline='',encoding='utf-8') as f:
    writer=csv.DictWriter(f,fieldnames=['id','titre','description','competences']);writer.writeheader();writer.writerows(rows)
profiles=[('Data Science','Python, Pandas, SQL, scikit-learn, Machine Learning','Analyse exploratoire et modèle de classification.'),('NLP','Python, NLP, Transformers, PyTorch, Hugging Face','Classification de textes et embeddings.'),('Data Engineering','Python, Spark, SQL, ETL, Elasticsearch','Pipeline de données et tableaux de bord.'),('Business Intelligence','SQL, Excel, Power BI, Python','Visualisation des indicateurs de performance.'),('Machine Learning','Python, FastAPI, Docker, Git, Machine Learning','Déploiement d’un modèle via une API.')]
for i in range(10):
    title,skills,project=profiles[i%len(profiles)]
    content=f'CV fictif {i+1}\nProfil : Étudiant en {title}\nCompétences : {skills}\nProjet : {project}\n'
    (root/'data'/'cvs'/f'cv_fictif_{i+1:02d}.txt').write_text(content,encoding='utf-8')
print('Créé : 50 offres et 10 CV fictifs (TXT).')
