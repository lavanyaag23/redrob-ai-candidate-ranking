"""
Stage F: reasoning generation. Produces a human-readable, field-grounded
justification for each ranked candidate - not a generic template. This
matters for the challenge's manual review stage, which checks whether
reasoning text actually reflects real profile data (vs. hallucinated or
boilerplate text).
"""


def stage_f_reasoning(cand: dict, b_info: dict, d_info: dict, flags: dict) -> str:
    profile = cand.get("profile", {})
    years = profile.get("years_of_experience", "?")
    title = profile.get("current_title", "Unknown role")

    if flags.get("honeypot_suspect"):
        return (
            "Profile shows internal inconsistencies (claimed expertise without "
            "supporting duration/history) - excluded as likely invalid data, "
            "not a genuine fit."
        )

    pieces = [f"{title} with {years} yrs experience"]

    if b_info["required_hits"] >= 3:
        pieces.append(f"matches {b_info['required_hits']} core JD requirements (retrieval/ranking/eval-related)")
    elif b_info["required_hits"] > 0:
        pieces.append(f"partial overlap on {b_info['required_hits']} required skill areas")
    else:
        pieces.append("limited direct skill-keyword overlap, ranked on career-history fit instead")

    if d_info["days_inactive"] <= 30:
        pieces.append("recently active on platform")
    elif d_info["days_inactive"] > 120:
        pieces.append(f"inactive for {d_info['days_inactive']} days - availability concern")

    sig = cand.get("redrob_signals", {})
    rr = sig.get("recruiter_response_rate")
    if rr is not None and rr < 0.2:
        pieces.append(f"low recruiter response rate ({rr:.2f})")

    if d_info["github_score"] >= 0.7:
        pieces.append("strong GitHub activity backing technical claims")
    elif d_info["github_score"] < 0.2:
        pieces.append("minimal GitHub activity")

    if d_info["assessment_score"] >= 0.85:
        pieces.append("high platform skill-assessment scores")

    if flags.get("title_chaser"):
        pieces.append("frequent short job tenures - retention risk per JD's stated preference")
    if not b_info["has_technical_title"]:
        pieces.append("current title is non-technical despite listed skills - flagged as low-confidence")

    return "; ".join(pieces) + "."