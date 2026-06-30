"""
Stage D: behavioral signal modifier. Combines redrob_signals (recency,
response rate, GitHub activity, skill assessments, verification, etc.)
into a single multiplier in the range [0.4, 1.0] that scales the rest of
the score - see ranking/score_fusion.py for why this is multiplicative
rather than additive.
"""

import numpy as np
from datetime import date, datetime


def parse_date_safe(s):
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except Exception:
        return None


def stage_d_behavioral_modifier(cand: dict, today: date = None) -> dict:
    if today is None:
        today = date.today()
    sig = cand.get("redrob_signals", {})

    last_active = parse_date_safe(sig.get("last_active_date"))
    days_inactive = (today - last_active).days if last_active else 9999

    recency_score = max(0.0, 1.0 - (days_inactive / 180.0))
    recency_score = min(recency_score, 1.0)

    response_rate = sig.get("recruiter_response_rate", 0.0) or 0.0
    interview_completion = sig.get("interview_completion_rate", 0.0) or 0.0
    open_to_work = 1.0 if sig.get("open_to_work_flag") else 0.5

    # offer_acceptance_rate can be -1 (no history) -> treat as neutral, not penalized
    offer_accept = sig.get("offer_acceptance_rate", -1)
    offer_accept_score = 0.5 if offer_accept == -1 else max(0.0, min(offer_accept, 1.0))

    verification_score = np.mean([
        1.0 if sig.get("verified_email") else 0.0,
        1.0 if sig.get("verified_phone") else 0.0,
        1.0 if sig.get("linkedin_connected") else 0.0,
    ])

    # avg_response_time_hours: faster reply -> higher engagement score.
    # <=4h is excellent, decaying to 0 by 7 days (168h). Missing -> neutral.
    resp_time = sig.get("avg_response_time_hours")
    if resp_time is None:
        response_speed_score = 0.5
    else:
        response_speed_score = max(0.0, 1.0 - (resp_time / 168.0))
        response_speed_score = min(response_speed_score, 1.0)

    # github_activity_score: -1 means no GitHub linked -> neutral, not
    # penalized (many strong engineers don't link GitHub on a recruiting
    # platform). 0-100 otherwise, scaled to 0-1.
    github_raw = sig.get("github_activity_score", -1)
    github_score = 0.5 if github_raw == -1 else max(0.0, min(github_raw / 100.0, 1.0))

    # skill_assessment_scores: average of any on-platform assessment scores.
    # Treated as an objective-evidence trust signal here, separate from the
    # keyword-overlap trust_multiplier in Stage B. Missing -> neutral.
    assess = sig.get("skill_assessment_scores", {}) or {}
    if assess:
        assessment_score = float(np.mean(list(assess.values()))) / 100.0
    else:
        assessment_score = 0.5

    behavioral_score = (
        0.22 * recency_score +
        0.18 * response_rate +
        0.10 * interview_completion +
        0.08 * open_to_work +
        0.05 * offer_accept_score +
        0.05 * verification_score +
        0.10 * response_speed_score +
        0.12 * github_score +
        0.10 * assessment_score
    )

    modifier = 0.4 + 0.6 * behavioral_score

    return {
        "behavioral_score": float(behavioral_score),
        "behavioral_modifier": float(modifier),
        "days_inactive": days_inactive,
        "github_score": float(github_score),
        "assessment_score": float(assessment_score),
        "response_speed_score": float(response_speed_score),
    }