"""Turn a messy Excel report into a clean table with real dates and numbers."""

from datetime import date, datetime
from pathlib import Path

import pandas as pd

from config import REQUIRED_COLUMNS
from excel_checker import extract_table, locate_table, read_sheets

# Rows starting with these words are summaries, not data
TOTAL_MARKERS = ("разом", "всього", "итого", "total")

# Text date formats we accept, tried in this order
DATE_FORMATS = ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y")


def parse_number(value) -> float | None:
    """125.5 / "125,50" / "1 250" -> float; anything else ("n/a", "") -> None."""
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return None if pd.isna(value) else float(value)
    # Remove normal, non-breaking and narrow spaces used as thousand separators
    text = str(value).strip().replace(" ", "").replace("\xa0", "").replace("\u202f", "")
    try:
        return float(text.replace(",", "."))
    except ValueError:
        return None


def parse_date(value) -> date | None:
    """Excel date / "2026-10-02" / "02.10.2026" -> date; unknown format -> None."""
    if isinstance(value, datetime):  # pandas Timestamp is a datetime too
        return value.date()
    if isinstance(value, date):
        return value
    if value is None:
        return None
    text = str(value).strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def is_total_row(row: pd.Series) -> bool:
    """True if any text cell of the row starts with a 'total' word."""
    return any(
        isinstance(v, str) and v.strip().lower().startswith(TOTAL_MARKERS)
        for v in row.values
    )


def load_report(path: Path) -> tuple[pd.DataFrame, list[str]]:
    """Read and clean one report. Returns (clean table, notes). Empty table = can't import."""
    notes: list[str] = []

    table = locate_table(read_sheets(path))
    if table is None:
        return pd.DataFrame(columns=REQUIRED_COLUMNS), ["header not found"]
    _, raw, header_row = table
    df, _, columns = extract_table(raw, header_row)

    missing = [c for c in REQUIRED_COLUMNS if c not in columns]
    if missing:
        return pd.DataFrame(columns=REQUIRED_COLUMNS), [f"missing columns: {', '.join(missing)}"]

    # Keep only the template columns, in the template order
    df = df[REQUIRED_COLUMNS].dropna(how="all")

    totals = df.apply(is_total_row, axis=1)
    if totals.any():
        notes.append(f"dropped {int(totals.sum())} total row(s)")
        df = df[~totals]

    # Convert types; values that can't be converted become None (validation catches them)
    df = df.assign(
        date=df["date"].map(parse_date),
        city=df["city"].map(lambda v: str(v).strip() if v is not None else None),
        product=df["product"].map(lambda v: str(v).strip() if v is not None else None),
        quantity=df["quantity"].map(parse_number),
        price=df["price"].map(parse_number),
    )
    if df.empty:
        notes.append("no data rows")

    # 1-based Excel row numbers help a human find the row in the original file
    df.insert(0, "excel_row", df.index + 1)
    return df.reset_index(drop=True), notes