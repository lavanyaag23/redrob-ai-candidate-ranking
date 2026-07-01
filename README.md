# Redrob AI Candidate Ranking System

AI-powered candidate ranking system developed for the **Redrob Data & AI Challenge**.

The system ranks candidates based on their relevance to a job description by combining rule-based matching, semantic similarity, behavioral signals, and explainable reasoning. It is designed to process **100,000 candidate profiles** efficiently while generating a transparent **Top-100 shortlist**.

---

## Motivation

Traditional recruitment systems rely heavily on keyword matching, which often overlooks qualified candidates or promotes irrelevant ones.

For example:

- A candidate who has built retrieval systems may never explicitly mention terms like **RAG** or **Pinecone**.
- Another candidate may list every trending AI keyword without having meaningful hands-on experience.

This project addresses that gap by combining semantic understanding with profile validation and behavioral signals to produce rankings recruiters can trust.

---

# Features

- Rule-based candidate filtering
- Semantic matching using Sentence Transformers
- Offline TF-IDF fallback
- Behavioral signal scoring
- Honeypot candidate detection
- Explainable candidate reasoning
- Top-100 candidate ranking
- Submission validator compatible with challenge requirements

---

# Ranking Pipeline

## Stage A — Hard Filtering

Filters or penalizes suspicious profiles based on:

- Impossible career timelines
- Unsupported skill claims
- Honeypot candidates
- Pure consulting backgrounds
- Pure research backgrounds
- Frequent job hopping
- Senior titles without recent technical work
- Non-NLP candidates lacking retrieval/search experience

---

## Stage B — Skill & Title Matching

Matches the job description against:

- Skills
- Job titles
- Career history

Rather than removing candidates with non-technical titles, the system applies score penalties to reduce the impact of keyword stuffing.

---

## Stage C — Semantic Matching

Calculates semantic similarity between:

- Job description
- Candidate summaries
- Career history

Supported backends:

- Sentence Transformers (`all-MiniLM-L6-v2`)
- TF-IDF + Cosine Similarity (offline mode)

This enables matching based on meaning instead of exact keywords.

---

## Stage D — Behavioral Signal Scoring

Candidate rankings are refined using platform engagement signals such as:

- Last active date
- Recruiter response rate
- Response speed
- Interview completion rate
- GitHub activity
- Skill assessment scores

---

## Stage E — Score Fusion

Final score is computed as:

```text
Final Score =
(Skill Score × Semantic Score) × Behavioral Modifier
```

Using a multiplicative behavioral modifier ensures inactive candidates are appropriately down-ranked rather than receiving only a small penalty.

---

## Stage F — Explainable Ranking

Every shortlisted candidate receives a concise explanation generated from profile data, including:

- Years of experience
- Current designation
- Matching skills
- Relevant work history
- Behavioral observations

This makes the ranking process transparent and recruiter-friendly.

---

# Project Structure

```text
redrob-ai-candidate-ranking/
│
├── data/
│   └── sample_candidates.jsonl
│
├── demo/
│   └── Syntax_Slayers_demo.mp4
│
├── docs/
│   ├── project-report.pdf
│   └── recruitment_pipeline_flowchart.png
│
├── outputs/
│
├── src/
│   ├── preprocessing/
│   ├── feature_engineering/
│   ├── matching/
│   ├── ranking/
│   ├── evaluation/
│   └── utils/
│
├── main.py
├── validate_submission.py
├── submission_metadata.yaml
├── requirements.txt
└── README.md
```

---

# Tech Stack

- Python
- Pandas
- NumPy
- scikit-learn
- Sentence Transformers
- TF-IDF
- Cosine Similarity

The project defaults to Sentence Transformers for semantic matching and automatically supports an offline TF-IDF backend.

---

# Getting Started

## Clone the Repository

```bash
git clone https://github.com/lavanyaag23/redrob-ai-candidate-ranking.git
cd redrob-ai-candidate-ranking
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Project

### Sample Dataset

```bash
python main.py \
    --candidates data/sample_candidates.jsonl \
    --out outputs/submission.csv \
    --backend tfidf
```

---

### Full Dataset

Place `candidates.jsonl` inside the `data/` folder.

```bash
python main.py \
    --candidates data/candidates.jsonl \
    --out outputs/submission.csv \
    --backend tfidf
```

Typical runtime:

- 70–85 seconds
- Single CPU core
- Less than 4 GB RAM

To enable sentence embeddings:

```bash
--backend embeddings
```

The model downloads only once and can then be used offline.

---

# Validate Submission

```bash
python validate_submission.py outputs/submission.csv
```

---

# Documentation

The `docs/` directory contains supporting project resources:

- **project-report.pdf** – Detailed project report explaining the methodology, implementation, and evaluation.
- **recruitment_pipeline_flowchart.png** – Architecture diagram illustrating the complete recruitment ranking pipeline.

---

# Demo

A demonstration video showcasing the complete workflow is available in:

```text
demo/
└── Syntax_Slayers_demo.mp4
```

---

# Live Demo

A lightweight version of the system (supports up to 100 candidates) is deployed on Hugging Face Spaces:

**https://huggingface.co/spaces/aditii14/redrob-candidate-ranker**

---

# Honeypot Detection

The dataset contains intentionally misleading candidate profiles.

The system detects these by analyzing inconsistencies such as:

- Impossible employment timelines
- Unsupported skill claims
- Unrealistic assessment records

Instead of silently removing them, the ranking algorithm heavily penalizes these candidates while preserving explainability.

---

# Evaluation

The solution was evaluated on:

- Submission format validation
- Honeypot rate within the Top-100
- Runtime performance
- Memory usage
- Manual verification of generated explanations

---

# Team

| Member | Contribution |
|---------|--------------|
| **Lavanya Agrawal** | System architecture, ranking logic, project integration |
| **Aahna Rathore** | Candidate schema analysis and feature engineering |
| **Saumya Bhalothia** | Job description analysis and semantic matching |
| **Aditi Kumari** | Pipeline implementation, security checks, submission validation |

---

# Future Improvements

Potential enhancements include:

- Learning-to-Rank models (LightGBM/XGBoost)
- Cross-Encoder reranking
- Domain-specific embedding models
- Improved behavioral calibration
- Enhanced explanation generation
- Interactive recruiter dashboard

---

# License

This project was developed for the **Redrob Data & AI Challenge** and is intended for educational and hackathon purposes.