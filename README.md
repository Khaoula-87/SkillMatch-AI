
# SkillMatch AI

### Intelligent CV and Internship Matching Using NLP

SkillMatch AI is an NLP-based application designed to analyze resumes and recommend internship opportunities based on their relevance to a candidate's skills and experience.

The project compares two Natural Language Processing approaches: **TF-IDF** and **Sentence-BERT**.

## Project Objectives

- Extract text automatically from PDF resumes.
- Identify technical skills using NLP techniques.
- Analyze internship descriptions.
- Rank job opportunities based on CV-job similarity.
- Identify matching and non-detected skills.
- Compare lexical and semantic matching approaches.
- Evaluate recommendation quality using ranking metrics.

## Technologies

- Python
- Streamlit
- Pandas and NumPy
- Scikit-learn
- Sentence-Transformers
- PyMuPDF
- TF-IDF and Cosine Similarity

## Dataset

The application uses a synthetic dataset created for academic experimentation.

- 50 internship offers
- 10 fictional CV profiles
- Job titles, descriptions, and required skills
- Relevance annotations for model evaluation

The synthetic data allows the matching pipeline to be tested without exposing personal information.

## NLP Pipeline

```text
PDF Resume
    |
    v
Text Extraction (PyMuPDF)
    |
    v
Text Preprocessing
    |
    v
Skill Extraction
    |
    v
TF-IDF / Sentence-BERT
    |
    v
Cosine Similarity
    |
    v
Job Ranking (Top K)
    |
    v
Matching and Non-Detected Skills
    |
    v
Streamlit Dashboard
```

## NLP Models

### TF-IDF

TF-IDF converts resumes and job descriptions into numerical vectors based on word importance.

Cosine similarity is then used to measure lexical similarity between documents.

### Sentence-BERT

Sentence-BERT generates dense semantic embeddings using the pretrained model:

`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`

Cosine similarity is used to rank job descriptions according to their semantic proximity to the CV.

## Model Evaluation

The models were evaluated using three ranking metrics:

| Metric | TF-IDF | Sentence-BERT |
|---|---:|---:|
| Precision@5 | 1.0000 | 1.0000 |
| Recall@5 | 0.2222 | 0.2222 |
| nDCG@5 | 1.0000 | 1.0000 |

These results were obtained using three fictional CVs and AI-generated relevance annotations.

The evaluation is exploratory. The synthetic and repetitive nature of the dataset limits the generalizability of the results.

## Application Features

The Streamlit application provides:

- PDF resume upload
- Automatic skill extraction
- Top K internship recommendations
- TF-IDF and Sentence-BERT comparison
- Matching and non-detected skill explanations
- Similarity score visualization
- Model evaluation dashboard
- CSV export

## Project Structure

```text
SkillMatch-AI/
├── data/
│   ├── cvs/
│   ├── offres.csv
│   └── annotations.csv
├── results/
│   ├── comparaison_modeles.csv
│   └── resume_evaluation.csv
├── src/
│   ├── preprocessing.py
│   ├── pdf_extractor.py
│   ├── skill_extractor.py
│   ├── tfidf_model.py
│   ├── sbert_model.py
│   ├── matching.py
│   └── evaluation.py
├── app.py
├── annotate.py
├── evaluate_models.py
├── generate_data.py
├── prepare_annotations.py
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Khaoula-87/SkillMatch-AI.git
cd SkillMatch-AI
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal.

## Evaluation

To reproduce the evaluation using the included annotations:

```bash
python evaluate_models.py
```

## Limitations and Future Work

- Evaluation on a small synthetic dataset
- Limited skill vocabulary
- AI-generated relevance labels
- No independent human validation

Future improvements include using real job descriptions, expanding the skill extraction system, adding experience-level filtering, and testing hybrid recommendation approaches.

## Contributors

- Khaoula BOUALI
- Loubna AMELLACHOU

## Project Context

Academic NLP mini-project focused on information retrieval, semantic similarity, and recommendation systems.
