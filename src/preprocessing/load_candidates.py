"""
Stage: data loading. Reads the line-delimited candidates.jsonl file into a
list of candidate dicts.
"""

import json
from pathlib import Path


def load_candidates(path: Path, limit: int = None) -> list:
    """Load candidates from a .jsonl file (one JSON object per line).

    Args:
        path: path to candidates.jsonl
        limit: if set, only load the first N rows (useful for quick local tests)
    """
    candidates = []
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if limit and i >= limit:
                break
            line = line.strip()
            if not line:
                continue
            candidates.append(json.loads(line))
    return candidates