"""
Stage C: semantic matching. Computes similarity between the JD text and
each candidate's career-history-derived text. Supports two backends:

- sentence-transformers embeddings (better quality, needs a one-time model
  download with internet access; ranking itself then runs fully offline)
- TF-IDF + cosine similarity (no model download required at all - useful
  for fully offline environments or quick local testing)
"""

import numpy as np

try:
    from sentence_transformers import SentenceTransformer
    HAS_ST = True
except ImportError:
    HAS_ST = False

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.utils.jd_config import JD_TEXT
from src.feature_engineering.build_features import build_candidate_text


def stage_c_semantic_scores(candidates: list, model=None) -> np.ndarray:
    """Returns an array of similarity scores in [0, 1], one per candidate,
    in the same order as `candidates`."""
    cand_texts = [build_candidate_text(c) for c in candidates]

    if model is not None and HAS_ST:
        jd_emb = model.encode([JD_TEXT], normalize_embeddings=True)
        cand_embs = model.encode(cand_texts, batch_size=64, show_progress_bar=True, normalize_embeddings=True)
        sims = cand_embs @ jd_emb.T
        sims = sims.flatten()
        sims = (sims + 1) / 2  # rescale [-1,1] -> [0,1]
        return sims

    # --- TF-IDF fallback ---
    corpus = [JD_TEXT] + cand_texts
    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000, ngram_range=(1, 2))
    tfidf = vectorizer.fit_transform(corpus)
    jd_vec = tfidf[0:1]
    cand_vecs = tfidf[1:]
    sims = cosine_similarity(cand_vecs, jd_vec).flatten()  # already in [0,1]
    return sims


def load_embedding_model(model_name: str = "all-MiniLM-L6-v2"):
    """Attempts to load a local sentence-transformers model. Returns None
    (caller should fall back to TF-IDF) if the model can't be loaded."""
    if not HAS_ST:
        return None
    try:
        return SentenceTransformer(model_name, device="cpu")
    except Exception:
        return None