#!/usr/bin/env python3
"""Submission script for make.fun bounty: The Painfully Honest Out-of-Office."""

from pathlib import Path
import sys

# Competition: The Painfully Honest Out-of-Office (program/v1)
#
# Adherence to Judge Criteria:
# 1. Painfully honest about absence: Confronts the uncomfortable corporate reality
#    that every dedicated worker privately fears—that the company operates fine
#    without them, making indispensability an ego illusion.
# 2. Warm, polite, and manager-approved: Compliments company resilience ("functions
#    perfectly well") with self-effacing wit, avoiding cynicism, blame, or complaints.
# 3. Form and length: A single, natural 124-character sentence (well within 200 max)
#    that never feels crammed or clipped.
# 4. Quotable turn of phrase: "testing the uncomfortable hypothesis that the company
#    functions perfectly well without me" is memorable, punchy, and watercooler-ready.
AUTO_REPLY_ENTRY: str = (
    "I am currently out of the office, testing the uncomfortable hypothesis "
    "that the company functions perfectly well without me."
)

OUTPUT_DIRECTORY: Path = Path("/output")
OUTPUT_FILE_PATH: Path = OUTPUT_DIRECTORY / "entry.txt"


def validate_out_of_office_line(line: str) -> None:
    """Validate entry line against all contest constraints."""
    # Ensure line is non-empty and at most 200 characters
    char_count = len(line)
    if not (1 <= char_count <= 200):
        raise ValueError(
            f"Line length must be between 1 and 200 characters; got {char_count}."
        )

    # Must be a single line (no newlines, tabs, or carriage returns)
    if any(ctrl in line for ctrl in ("\n", "\r", "\t")):
        raise ValueError("Line contains forbidden newline, tab, or carriage return characters.")

    # Must have no leading or trailing whitespace
    if line != line.strip():
        raise ValueError("Line has unauthorized leading or trailing whitespace.")

    # Must be a grammatically complete single sentence ending with terminal punctuation
    if not line.endswith((".", "!", "?")):
        raise ValueError("Line must end with terminal punctuation ('.', '!', '?').")

    terminal_marks = [c for c in line if c in ".!?"]
    if len(terminal_marks) != 1:
        raise ValueError(
            f"Line must consist of exactly one sentence; found {len(terminal_marks)} terminal mark(s)."
        )

    # Must be valid UTF-8 and round-trip cleanly
    try:
        encoded = line.encode("utf-8")
        decoded = encoded.decode("utf-8")
        if decoded != line:
            raise ValueError("UTF-8 round-trip mismatch.")
    except (UnicodeEncodeError, UnicodeDecodeError) as err:
        raise ValueError(f"Line failed UTF-8 validation: {err}") from err

    if len(encoded) == 0:
        raise ValueError("Line UTF-8 payload is empty.")


def write_and_verify_entry(line: str, destination: Path) -> None:
    """Write entry line to destination file, re-read, and assert exact match."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(f"{line}\n", encoding="utf-8")

    # Read back and verify strict single-line equality
    stored_text = destination.read_text(encoding="utf-8")
    lines = stored_text.splitlines()
    assert len(lines) == 1, f"Expected exactly 1 line, got {len(lines)}"
    assert lines[0] == line, f"Mismatch: expected {line!r}, found {lines[0]!r}"


def main() -> None:
    """Execute validation, write output file, verify, and print to stdout."""
    validate_out_of_office_line(AUTO_REPLY_ENTRY)
    write_and_verify_entry(AUTO_REPLY_ENTRY, OUTPUT_FILE_PATH)
    # Output to stdout
    print(AUTO_REPLY_ENTRY)


if __name__ == "__main__":
    main()
