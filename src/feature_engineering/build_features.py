"""
Stage: feature engineering. Builds the text representation of a candidate
that gets fed into the semantic matching stage (Stage C).
"""


def build_candidate_text(cand: dict) -> str:
    """Concatenate the parts of a candidate's profile that carry the most
    signal about role fit: headline, summary, current title, and the most
    recent few job descriptions. Capped at 4 most-recent roles to keep the
    embedding input a manageable size."""
    profile = cand.get("profile", {})
    career = cand.get("career_history", [])
    parts = [
        profile.get("headline", ""),
        profile.get("summary", ""),
        profile.get("current_title", ""),
    ]
    for job in career[:4]:
        parts.append(job.get("title", ""))
        parts.append(job.get("description", ""))
    return " . ".join(p for p in parts if p)