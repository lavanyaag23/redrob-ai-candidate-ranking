"""
Stage E: score fusion. Combines the skill score (Stage B), semantic score
(Stage C), and behavioral modifier (Stage D) into one final score, applying
penalties for any hard-filter flags (Stage A).

Why multiplicative, not additive:
The job description explicitly says a perfect-on-paper candidate who hasn't
been active in months "is, for hiring purposes, not actually available" and
should be "down-weighted appropriately." An additive formula
(skill + semantic + behavioral) only lets a poor behavioral score drag the
total down by its own small slice - a stale, unresponsive candidate with
great skills can still rank highly. A multiplicative modifier (behavioral
score scales the rest of the score by 0.4x-1.0x) makes unavailability
proportionally suppress the whole score, matching what the JD asked for.
"""

import numpy as np


def stage_e_combine(skill_score: float, semantic_score: float, modifier: float, flags: dict) -> float:
    base = 0.45 * skill_score + 0.55 * semantic_score

    # Hard disqualifier penalties (soft-zero, not literal zero - the JD
    # treats some disqualifiers as harder than others)
    if flags["pure_research_only"]:
        base *= 0.05
    if flags["pure_consulting_only"]:
        base *= 0.15
    if flags["non_nlp_only"]:
        base *= 0.15
    if flags["senior_not_coding"]:
        base *= 0.3
    if flags["title_chaser"]:
        base *= 0.6
    if flags["honeypot_suspect"]:
        base *= 0.02  # near-zero - the critical honeypot defense

    final = base * modifier
    return float(np.clip(final, 0.0, 1.0))