"""Entry generator for make.fun bounty: 'The Painfully Honest Out-of-Office'."""

from pathlib import Path

ENTRY: str = (
    "I am currently out of the office, testing the uncomfortable hypothesis "
    "that the company functions perfectly well without me."
)


def validate_entry(text: str) -> None:
    """Validate entry against all competition criteria."""
    length = len(text)
    if not (1 <= length <= 200):
        raise ValueError(
            f"Validation failed: entry length must be between 1 and 200 characters, got {length}."
        )
    if "\n" in text or "\r" in text:
        raise ValueError(
            "Validation failed: entry must be a single line without newline or carriage return."
        )
    if text != text.strip():
        raise ValueError(
            "Validation failed: entry has unauthorized leading or trailing whitespace."
        )
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError(
            f"Validation failed: entry must be valid UTF-8 encodable text: {exc}"
        ) from exc


def main() -> None:
    validate_entry(ENTRY)

    output_dir = Path("/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / "entry.txt"

    out_file.write_text(f"{ENTRY}\n", encoding="utf-8")

    # Read back and assert it matches the entry exactly
    content = out_file.read_text(encoding="utf-8")
    lines = content.splitlines()
    assert len(lines) == 1, f"Expected exactly 1 line, got {len(lines)}"
    assert lines[0] == ENTRY, (
        f"Entry does not match: expected {ENTRY!r}, got {lines[0]!r}"
    )

    # Print the line to stdout
    print(ENTRY)


if __name__ == "__main__":
    main()
