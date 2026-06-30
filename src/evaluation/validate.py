"""
Stage: evaluation. This module wraps the organizer-provided
`validate_submission.py` script so it can be invoked programmatically from
main.py after ranking completes.

IMPORTANT: this does not replace or modify the original organizer file.
The unmodified `validate_submission.py` must still live at the repo root
exactly as provided - that is the file the organizers will actually run
against your submission. This wrapper just lets main.py call it
automatically as a self-check after generating outputs/submission.csv.
"""

import subprocess
import sys
from pathlib import Path


def run_validator(submission_csv: Path, validator_script: Path = None) -> bool:
    """Runs the organizer's validate_submission.py against a generated
    submission file. Returns True if validation passed, False otherwise.
    Prints the validator's own output either way."""
    if validator_script is None:
        # default: repo root, two levels up from src/evaluation/
        validator_script = Path(__file__).resolve().parents[2] / "validate_submission.py"

    if not validator_script.exists():
        print(f"Validator script not found at {validator_script}", file=sys.stderr)
        return False

    result = subprocess.run(
        [sys.executable, str(validator_script), str(submission_csv)],
        capture_output=True, text=True,
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    return result.returncode == 0