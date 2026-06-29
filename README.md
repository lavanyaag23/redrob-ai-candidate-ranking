# 🚀 Redrob AI Candidate Ranking System

> AI-powered Intelligent Candidate Discovery & Ranking System built for the **Redrob Data & AI Challenge**.

---

## 📌 Project Overview

Hiring the right candidate is more than matching keywords.

This project builds an **AI-powered Candidate Discovery & Ranking System** that intelligently ranks candidates by combining:

- Rule-based filtering
- Semantic AI matching
- Behavioral signal analysis
- Explainable AI recommendations

Instead of relying only on keyword matching, our system understands the **meaning** of the Job Description and Candidate Profiles to recommend the most suitable candidates.

---

## 🎯 Problem Statement

Given:

- 📄 Job Description (JD)
- 👨‍💻 100K Candidate Profiles

Build an intelligent ranking engine that:

- Identifies the best candidates
- Avoids keyword-only matching
- Detects honeypot/fake profiles
- Considers recruiter behavior signals
- Generates explainable recommendations
- Produces the Top 100 ranked candidates

---

# 🏗️ System Architecture

```
Job Description
        │
        ▼
JD Feature Extraction
        │
        ▼
Candidate Dataset
        │
        ▼
Feature Engineering
        │
        ▼
Hard Filters & Honeypot Detection
        │
        ▼
Rule-Based Matching
        │
        ▼
Semantic AI Matching
        │
        ▼
Behavioral Signal Scoring
        │
        ▼
Hybrid Score Fusion
        │
        ▼
Candidate Ranking
        │
        ▼
Explainable AI
        │
        ▼
submission.csv
```

---

# ✨ Key Features

✅ Intelligent Candidate Ranking

✅ Semantic Matching using Sentence Transformers

✅ Rule-Based Skill Matching

✅ Candidate Experience Analysis

✅ Behavioral Signal Analysis

✅ Explainable AI Recommendations

✅ Honeypot Candidate Detection

✅ Hybrid Scoring Pipeline

---

# 📂 Project Structure

```
redrob-ai-candidate-ranking/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│   ├── architecture.md
│   ├── candidate_schema_analysis.md
│   ├── jd_analysis.md
│   └── ranking_logic.md
│
├── notebooks/
│
├── src/
│   ├── preprocessing/
│   ├── feature_engineering/
│   ├── matching/
│   ├── ranking/
│   ├── evaluation/
│   └── utils/
│
├── outputs/
│
├── models/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙️ Tech Stack

### Programming Language

- Python

### Data Processing

- Pandas
- NumPy

### Machine Learning

- Scikit-learn

### NLP & Semantic Search

- Sentence Transformers
- all-MiniLM-L6-v2

### Similarity

- Cosine Similarity

### Version Control

- Git
- GitHub

---

# 🧠 Ranking Pipeline

### Stage 1

Candidate Parsing & Feature Extraction

### Stage 2

Hard Filters

- Invalid Profiles
- Honeypot Detection
- JD Disqualifiers

### Stage 3

Rule-Based Matching

- Skills
- Titles
- Experience
- Education

### Stage 4

Semantic AI Matching

- Candidate Summary
- Career History
- Job Description

### Stage 5

Behavioral Scoring

- Open to Work
- Last Active
- Recruiter Response Rate
- GitHub Activity
- Interview Completion

### Stage 6

Hybrid Score Fusion

```
Final Score =
Rule Score
+ Semantic Score
+ Behavioral Score
```

### Stage 7

Top 100 Candidate Selection

### Stage 8

Explainable Recommendation Generation

---

# 📊 Evaluation Metrics

- Precision@100
- Honeypot Detection Rate
- Semantic Match Quality
- Behavioral Ranking Quality
- Score Distribution Analysis

---

# 👥 Team

| Member | Role |
|----------|------|
| Lavanya Agrawal | Project Architecture, Ranking Logic, Integration |
| Ahana Rathore| Feature Engineering |
| Saumya Bhalothia | Job Description Analysis & Semantic Matching |
| Aditi Kumari | Data Processing & Validation |

---

# 🚀 Getting Started

Clone the repository

```bash
git clone https://github.com/<your-username/redrob-ai-candidate-ranking.git
```

Move into the project

```bash
cd redrob-ai-candidate-ranking
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the project

```bash
python main.py
```

---

# 📌 Future Improvements

- Learning-to-Rank Models
- XGBoost Ranker
- Fine-tuned Embedding Models
- LLM-based Candidate Reasoning
- Interactive Recruiter Dashboard
- Real-time Candidate Search API

---

# 📄 License

This project is developed for the **Redrob Data & AI Challenge** for educational and hackathon purposes.

---

## ⭐ If you found this project interesting, don't forget to star the repository!
