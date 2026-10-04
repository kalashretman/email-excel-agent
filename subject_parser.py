"""Parse report email subjects like 'Report 2026-09-30 Kyiv'."""


def parse_subject(subject: str) -> dict[str, str] | None:
    """Return {"date": ..., "city": ...} or None if the subject doesn't match."""
    # Split into at most 3 parts; split() ignores repeated spaces
    parts = subject.strip().split(maxsplit=2)

    # Check the count BEFORE unpacking, otherwise we get a ValueError
    if len(parts) != 3:
        return None

    keyword, date, city = parts

    # The first word must be "report", case-insensitive
    if keyword.lower() != "report":
        return None

    # Basic YYYY-MM-DD format check
    if len(date) != 10 or date[4] != "-" or date[7] != "-":
        return None

    return {"date": date, "city": city}


if __name__ == "__main__":
    # Quick self-test: runs only when this file is executed directly
    for s in ["Report 2026-09-30 Kyiv", "Invoice 2026-09-30 Kyiv", ""]:
        print(f"{s!r:<28} -> {parse_subject(s)}")