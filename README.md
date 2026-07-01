# Redrob AI Candidate Ranking System

AI-powered candidate ranking system built for the Redrob Data & AI Challenge.

## Why this approach

Recruiters go through hundreds of profiles and still miss good candidates — not because the talent isn't there, but because keyword filters can't see what actually matters. A candidate who built a recommendation system at a product company might never use the word "RAG" or "Pinecone" on their profile. A candidate who lists every AI buzzword as a skill but has a Marketing Manager title probably isn't a fit. Plain keyword matching can't tell these two apart; this system tries to.

Given a job description and 100,000 candidate profiles, the goal is to produce a ranked top-100 shortlist that a recruiter could actually trust — not just filtered, but ranked, with reasoning a human can check against the candidate's real history.

## How it works

The pipeline runs in six stages:

**Stage A — Hard filters.** Flags honeypot/fabricated profiles (e.g. "expert" proficiency claimed with zero months of duration, career timelines that don't add up) and the disqualifiers the JD calls out explicitly: pure-research-only backgrounds, pure-consulting-only career history, non-NLP domains with no retrieval/search exposure, frequent job-hopping, and senior titles with no evidence of recent hands-on coding.

**Stage B — Rule-based skill and title matching.** Checks the JD's required and preferred skill terms against the candidate's skills list, career history text, and current title. Candidates whose title doesn't reflect technical work get a discount here (not a hard cutoff) — this is the direct defense against the keyword-stuffer trap the JD describes.

**Stage C — Semantic matching.** Compares the JD text against each candidate's summary and career history using sentence embeddings (or TF-IDF as an offline-safe fallback). This is what catches the "plain-language" candidates — the ones who did the right work without using the JD's exact vocabulary.

**Stage D — Behavioral signal scoring.** Pulls in last-active recency, recruiter response rate and response speed, interview completion rate, GitHub activity score, and platform skill-assessment scores from `redrob_signals`.

**Stage E — Score fusion.**

```
final_score = (skill_score × semantic_score) × behavioral_modifier
```

This is multiplicative, not additive, and that was a deliberate choice. The JD says directly that a perfect-on-paper candidate who hasn't logged in for months "is, for hiring purposes, not actually available" and should be down-weighted accordingly. An additive formula only lets a weak behavioral score subtract a small, fixed slice off the total — a candidate with great skills but zero engagement could still rank near the top. Making the behavioral signal a multiplier (scaling the rest of the score by roughly 0.4x to 1.0x) means low availability actually suppresses the score proportionally, which is what the JD is asking for.

**Stage F — Reasoning generation.** Every ranked candidate gets a short, grounded explanation built from their real profile fields — years of experience, title, which specific JD requirements matched, and any behavioral concerns. Nothing here is templated boilerplate; it's assembled per-candidate from what's actually in their data.

## Project structure

```
redrob-ai-candidate-ranking/
├── data/
│   └── sample_candidates.jsonl    # small sample for local testing (full candidates.jsonl
│                                    # is not committed — see Getting Started)
├── src/
│   ├── preprocessing/              # candidate loading
│   ├── feature_engineering/        # candidate text construction for embeddings
│   ├── matching/                   # Stages A-C
│   ├── ranking/                    # Stages D-F
│   ├── evaluation/                 # wraps the organizer's validator
│   └── utils/                      # JD text, skill term lists, shared constants
├── outputs/                        # submission.csv lands here when generated
├── main.py                         # CLI entrypoint
├── validate_submission.py          # organizer-provided format validator
├── submission_metadata.yaml
├── requirements.txt
└── README.md
```

## Tech stack

Python, pandas, NumPy, scikit-learn. Semantic matching uses sentence-transformers (`all-MiniLM-L6-v2`) by default, with a TF-IDF + cosine similarity fallback that needs no model download and runs fully offline — useful if you want to avoid the one-time model download or are testing in a no-network environment.

## Getting started

```bash
git clone https://github.com/lavanyaag23/redrob-ai-candidate-ranking.git
cd redrob-ai-candidate-ranking
pip install -r requirements.txt
```

Quick test on the bundled sample (50 candidates, runs in well under a second):

```bash
python main.py --candidates data/sample_candidates.jsonl --out outputs/submission.csv --backend tfidf
```

Full run on the actual 100K dataset — place `candidates.jsonl` in `data/` first (it's not committed here, ~490MB):

```bash
python main.py --candidates data/candidates.jsonl --out outputs/submission.csv --backend tfidf
```

This produces the top-100 ranked `submission.csv`. On a single CPU core this takes roughly 70-85 seconds, comfortably inside the 5-minute compute budget. Swap `--backend tfidf` for `--backend embeddings` if you want the sentence-transformers backend instead — it needs an internet connection the first time to download the model, but ranking itself still runs offline after that.

Check the output against the official spec:

```bash
python validate_submission.py outputs/submission.csv
```

## Sandbox / demo

A small-sample version of this pipeline (accepts up to 100 candidates, runs end-to-end) is hosted here for quick verification:

https://huggingface.co/spaces/aditii14/redrob-candidate-ranker

## Honeypot handling

The dataset includes a small number of honeypot candidates with profiles that look fine on the surface but don't hold up — impossible tenure, skill claims with no supporting history, assessment scores with nothing behind them. Stage A flags these and Stage E pushes their score close to zero rather than dropping them silently, so the scoring stays traceable end to end.

## Evaluation we ran locally

- Honeypot rate in the top 100 (target: under the 10% disqualification threshold)
- Format and tie-break validation via `validate_submission.py`
- Runtime/memory on the full 100K set: ~70-85 seconds, single core, under 4GB RAM
- Manual spot-checks of reasoning text against the actual candidate profiles, to catch anything that looked templated or hallucinated

## Team

| Member | Role |
|---|---|
| Lavanya Agrawal | Architecture, ranking logic, integration |
| Aahna Rathore | Candidate schema and feature analysis |
| Saumya Bhalothia | Job description analysis, semantic matching |
| Aditi Kumari | Pipeline implementation, submission validation |

## Possible next steps

A learned ranking model (e.g. LightGBM/XGBoost) trained on labeled relevance judgments instead of hand-tuned weights, a fine-tuned domain embedding model, and richer per-candidate reasoning would all be natural follow-ups given more time.

## License

Built for the Redrob Data & AI Challenge, for hackathon and educational purposes.
>>>>>>> eeeb300cba1064e57209bd4bf58c1ed3400f43f0
