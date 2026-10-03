def parse_subject(subject):
    """Parse an email subject like 'Report YYYY-MM-DD City'.

    Returns {"date": ..., "city": ...} or None if the subject doesn't match.
    """
    # 1. Strip leading/trailing whitespace (like trim() in PHP)
    subject = subject.strip()

    # 2. Split into at most 3 parts: maxsplit=2 means 2 cuts.
    #    split() with no argument ignores repeated spaces.
    parts = subject.split(maxsplit=2)

    # 3. Check the count BEFORE unpacking, otherwise we get a ValueError
    if len(parts) != 3:
        return None

    # 4. Unpack into variables (like [$keyword, $date, $city] = $parts in PHP)
    keyword, date, city = parts

    # 5. The first word must be "report", case-insensitive
    if keyword.lower() != "report":
        return None

    # 6. Basic YYYY-MM-DD date format check
    if len(date) != 10 or date[4] != "-" or date[7] != "-":
        return None

    # 7. All checks passed: return a dict (like an associative array in PHP)
    return {"date": date, "city": city}


if __name__ == "__main__":
    subjects = [
        "Report 2026-09-30 Kyiv",
        "  report 2026-09-30   Lviv  ",
        "Report 2026-10-01 Kryvyi Rih",
        "REPORT 2026-10-02 Ivano-Frankivsk",
        "Invoice 2026-09-30 Kyiv",
        "Report Kyiv",
        "Report 30.09.2026 Kyiv",
        "",
    ]

    for subject in subjects:
        result = parse_subject(subject)
        if result is None:
            print(f"SKIP | {subject!r}")
        else:
            print(f"OK   | {subject!r:<36} -> date={result['date']}, city={result['city']}")