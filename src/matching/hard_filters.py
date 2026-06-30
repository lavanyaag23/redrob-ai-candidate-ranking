"""
Stage A: hard filters. Flags honeypot/fabricated profiles and JD-stated
disqualifiers. Returns boolean flags rather than dropping rows outright -
Stage E (score fusion) applies the actual penalties, since some
disqualifiers should heavily suppress a score rather than hard-remove it.
"""

import numpy as np

from src.utils.jd_config import (
    PURE_RESEARCH_TERMS,
    PURE_CONSULTING_FIRMS,
    NON_NLP_DOMAINS,
    NLP_IR_TERMS,
    TITLE_HOP_MAX_AVG_MONTHS,
    NON_CODING_SENIOR_TITLES,
)


def stage_a_flags(cand: dict) -> dict:
    flags = {
        "honeypot_suspect": False,
        "pure_research_only": False,
        "pure_consulting_only": False,
        "non_nlp_only": False,
        "title_chaser": False,
        "senior_not_coding": False,
    }

    skills = cand.get("skills", [])
    career = cand.get("career_history", [])
    profile = cand.get("profile", {})

    # --- Honeypot heuristic 1: "expert" proficiency with 0 duration_months ---
    for sk in skills:
        if sk.get("proficiency") == "expert" and sk.get("duration_months", 0) == 0:
            flags["honeypot_suspect"] = True
            break

    # --- Honeypot heuristic 2: a single job's duration implausibly exceeds
    # the candidate's total claimed years of experience ---
    total_years = profile.get("years_of_experience", 0)
    for job in career:
        dm = job.get("duration_months", 0) or 0
        if dm / 12.0 > total_years + 1:  # +1 buffer for rounding
            flags["honeypot_suspect"] = True
            break

    # --- Honeypot heuristic 3: very high skill_assessment_scores for skills
    # that appear nowhere in skills[] or career-history text ---
    sig = cand.get("redrob_signals", {})
    assess = sig.get("skill_assessment_scores", {})
    skill_names_lower = {s.get("name", "").lower() for s in skills}
    career_text_blob = " ".join(j.get("description", "") for j in career).lower()
    for skill_name, score in assess.items():
        if score and score >= 90:
            sname = skill_name.lower()
            if sname not in skill_names_lower and sname not in career_text_blob:
                flags["honeypot_suspect"] = True
                break

    titles_text = " ".join(j.get("title", "") for j in career).lower()
    industries_text = " ".join(j.get("industry", "") for j in career).lower()

    # --- Pure research only (no industry/production signal at all) ---
    if any(t in titles_text for t in PURE_RESEARCH_TERMS):
        if "product" not in industries_text and not any(
            kw in career_text_blob for kw in ["deployed", "production", "shipped", "users"]
        ):
            flags["pure_research_only"] = True

    # --- Pure consulting only (every job at a known consulting firm) ---
    companies = [j.get("company", "").lower() for j in career]
    if companies and all(any(f in c for f in PURE_CONSULTING_FIRMS) for c in companies):
        flags["pure_consulting_only"] = True

    # --- Non-NLP domain only (CV/speech/robotics without NLP/IR exposure) ---
    if any(term in career_text_blob or term in titles_text for term in NON_NLP_DOMAINS):
        if not any(term in career_text_blob for term in NLP_IR_TERMS):
            flags["non_nlp_only"] = True

    # --- Title chaser: short average tenure across 3+ jobs ---
    if len(career) >= 3:
        durations = [j.get("duration_months", 0) or 0 for j in career]
        avg_months = sum(durations) / len(durations)
        if avg_months > 0 and avg_months < TITLE_HOP_MAX_AVG_MONTHS:
            flags["title_chaser"] = True

    # --- Senior but not coding: architect/lead/manager title AND current job
    # description has no hands-on coding language ---
    current_title = profile.get("current_title", "").lower()
    if any(t in current_title for t in NON_CODING_SENIOR_TITLES):
        current_job = next((j for j in career if j.get("is_current")), None)
        if current_job:
            desc = current_job.get("description", "").lower()
            coding_signals = ["implemented", "built", "wrote", "coded", "developed", "shipped code"]
            if not any(s in desc for s in coding_signals):
                flags["senior_not_coding"] = True

    return flags