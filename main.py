#!/usr/bin/env python3
"""
Redrob Hackathon — Candidate Ranking Pipeline (entrypoint)
============================================================

Orchestrates Stages A-F across the modules in src/:

  A. src/matching/hard_filters.py      — honeypot & disqualifier flags
  B. src/matching/skill_match.py        — rule-based skill/title score
  C. src/matching/semantic_match.py     — semantic similarity (embeddings or TF-IDF)
  D. src/ranking/behavioral.py          — behavioral signal modifier
  E. src/ranking/score_fusion.py        — multiplicative combination
  F. src/ranking/reasoning.py           — grounded reasoning text

Usage:
    python main.py --candidates data/candidates.jsonl --out outputs/submission.csv [--backend tfidf|embeddings|auto] [--limit N]

After writing the output, automatically runs the organizer's
validate_submission.py against it (unless --skip-validate is passed).
"""

import argparse
import sys
from pathlib import Path

import pandas as pd

from src.preprocessing.load_candidates import load_candidates
from src.matching.hard_filters import stage_a_flags
from src.matching.skill_match import stage_b_skill_score
from src.matching.semantic_match import stage_c_semantic_scores, load_embedding_model
from src.ranking.behavioral import stage_d_behavioral_modifier
from src.ranking.score_fusion import stage_e_combine
from src.ranking.reasoning import stage_f_reasoning
from src.evaluation.validate import run_validator


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--limit", type=int, default=None, help="Only load first N rows (testing)")
    ap.add_argument("--model", default="all-MiniLM-L6-v2")
    ap.add_argument("--backend", choices=["auto", "embeddings", "tfidf"], default="auto",
                    help="'embeddings' forces sentence-transformers, 'tfidf' forces the "
                         "offline fallback, 'auto' tries embeddings and falls back to tfidf")
    ap.add_argument("--skip-validate", action="store_true",
                    help="skip running validate_submission.py after ranking")
    args = ap.parse_args()

    print(f"Loading candidates from {args.candidates} ...", file=sys.stderr)
    candidates = load_candidates(args.candidates, limit=args.limit)
    print(f"Loaded {len(candidates)} candidates.", file=sys.stderr)

    model = None
    if args.backend in ("auto", "embeddings"):
        print("Attempting to load embedding model (local, CPU) ...", file=sys.stderr)
        model = load_embedding_model(args.model)
        if model is None:
            if args.backend == "embeddings":
                print("ERROR: could not load embedding model and --backend embeddings was forced.", file=sys.stderr)
                sys.exit(1)
            print("Could not load embedding model; falling back to TF-IDF.", file=sys.stderr)
    if model is None:
        print("Using TF-IDF backend for Stage C (no model download required).", file=sys.stderr)

    print("Stage C: computing semantic similarity ...", file=sys.stderr)
    semantic_scores = stage_c_semantic_scores(candidates, model)

    rows = []
    for cand, sem_score in zip(candidates, semantic_scores):
        flags = stage_a_flags(cand)
        b_info = stage_b_skill_score(cand)
        d_info = stage_d_behavioral_modifier(cand)
        final_score = stage_e_combine(
            b_info["skill_score"], float(sem_score), d_info["behavioral_modifier"], flags
        )
        reasoning = stage_f_reasoning(cand, b_info, d_info, flags)
        rows.append({
            "candidate_id": cand["candidate_id"],
            "score": final_score,
            "reasoning": reasoning,
        })

    df = pd.DataFrame(rows)
    df["score_rounded"] = df["score"].round(4)
    # Sort by the ROUNDED score (what the validator checks), then
    # candidate_id ascending as the deterministic tie-break.
    df = df.sort_values(["score_rounded", "candidate_id"], ascending=[False, True]).reset_index(drop=True)

    top100 = df.head(100).copy()
    top100["rank"] = range(1, len(top100) + 1)
    top100["score"] = top100["score_rounded"]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    out_df = top100[["candidate_id", "rank", "score", "reasoning"]]
    out_df.to_csv(args.out, index=False)
    print(f"Wrote {len(out_df)} ranked rows to {args.out}", file=sys.stderr)

    if not args.skip_validate:
        print("\nRunning organizer's validate_submission.py ...", file=sys.stderr)
        ok = run_validator(args.out)
        if not ok:
            print("Validation FAILED - see output above.", file=sys.stderr)
            sys.exit(1)
        print("Validation passed.", file=sys.stderr)


if __name__ == "__main__":
    main()