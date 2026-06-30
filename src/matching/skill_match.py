"""
Stage B: rule-based skill and title matching. Checks the JD's required and
preferred skill terms against the candidate's skills list, career-history
text, and title - then applies a title-sanity discount (not a hard cutoff)
for candidates whose title doesn't reflect technical work, since the JD's
keyword-stuffer trap example is exactly "all the AI keywords as skills but
title is Marketing Manager".
"""

import numpy as np

from src.utils.jd_config import REQUIRED_SKILL_TERMS, PREFERRED_SKILL_TERMS, TECHNICAL_TITLE_TERMS


def stage_b_skill_score(cand: dict) -> dict:
    skills = cand.get("skills", [])
    career = cand.get("career_history", [])
    profile = cand.get("profile", {})

    skill_names = [s.get("name", "").lower() for s in skills]
    skills_blob = " ".join(skill_names)
    career_text = " ".join(j.get("description", "") for j in career).lower()
    title_text = (profile.get("current_title", "") + " " + " ".join(j.get("title", "") for j in career)).lower()
    full_text = skills_blob + " " + career_text + " " + title_text + " " + profile.get("summary", "").lower()

    required_hits = sum(1 for term in REQUIRED_SKILL_TERMS if term in full_text)
    preferred_hits = sum(1 for term in PREFERRED_SKILL_TERMS if term in full_text)

    required_score = min(required_hits / 6.0, 1.0)  # ~6 distinct required-term hits = full score
    preferred_score = min(preferred_hits / 4.0, 1.0)

    # Title sanity check: does the title reflect technical IR/ML work?
    # This is the direct counter to the JD's stated keyword-stuffer trap -
    # a discount, not a hard floor, so it scales rather than zeroing out.
    has_technical_title = any(t in title_text for t in TECHNICAL_TITLE_TERMS)
    title_multiplier = 1.0 if has_technical_title else 0.25

    # Skill-claim trust: do the claimed skills have endorsement/duration
    # backing, or are they just listed with 0 duration?
    relevant_skills = [s for s in skills if s.get("name", "").lower() in
                        " ".join(REQUIRED_SKILL_TERMS + PREFERRED_SKILL_TERMS)]
    if relevant_skills:
        avg_duration = np.mean([s.get("duration_months", 0) or 0 for s in relevant_skills])
        trust_multiplier = min(avg_duration / 24.0, 1.0)  # 24 months = full trust
        trust_multiplier = max(trust_multiplier, 0.3)  # floor, don't zero out entirely
    else:
        trust_multiplier = 0.5

    skill_score = (0.7 * required_score + 0.3 * preferred_score) * trust_multiplier * title_multiplier

    return {
        "skill_score": float(skill_score),
        "required_hits": required_hits,
        "preferred_hits": preferred_hits,
        "has_technical_title": has_technical_title,
    }