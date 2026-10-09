"""Check an Excel report against the expected template: sheet, header, columns, values."""

from pathlib import Path

import pandas as pd

from config import COLUMN_ALIASES, HEADER_SEARCH_ROWS, NUMERIC_COLUMNS, REQUIRED_COLUMNS

# Every name we can recognize: standard names + their aliases
KNOWN_NAMES = set(REQUIRED_COLUMNS) | set(COLUMN_ALIASES)


def normalize_column(name) -> str:
    """'  Qty ' -> 'quantity': trim, lowercase, then map known aliases."""
    clean = str(name).strip().lower()
    return COLUMN_ALIASES.get(clean, clean)


def read_sheets(path: Path) -> dict[str, pd.DataFrame]:
    """Read ALL sheets as raw data (no header). Only truly empty cells become missing."""
    # keep_default_na=False: otherwise pandas silently turns "n/a", "NA", "null"
    # into empty values and we never see that the partner wrote garbage there.
    sheets = pd.read_excel(path, sheet_name=None, header=None, keep_default_na=False)
    return {name: raw.replace("", None) for name, raw in sheets.items()}


def find_header_row(raw: pd.DataFrame) -> tuple[int | None, int]:
    """Return (index of the row that looks most like a header, number of matches)."""
    best_row, best_hits = None, 0
    for i in range(min(HEADER_SEARCH_ROWS, len(raw))):
        # Count cells in this row that match a known column name
        cells = [str(v).strip().lower() for v in raw.iloc[i] if not pd.isna(v)]
        hits = sum(1 for c in cells if c in KNOWN_NAMES)
        if hits > best_hits:
            best_row, best_hits = i, hits
    # Require at least half of the template to call it a header
    if best_hits < len(REQUIRED_COLUMNS) / 2:
        return None, 0
    return best_row, best_hits


def locate_table(sheets: dict[str, pd.DataFrame]) -> tuple[str, pd.DataFrame, int] | None:
    """Find the sheet with the best header. Returns (sheet name, raw data, header row)."""
    best = None
    for name, raw in sheets.items():
        row, hits = find_header_row(raw)
        if row is not None and (best is None or hits > best[3]):
            best = (name, raw, row, hits)
    return None if best is None else best[:3]


def extract_table(raw: pd.DataFrame, header_row: int) -> tuple[pd.DataFrame, list[str], list[str]]:
    """Cut the data below the header. Returns (data, original names, normalized names)."""
    original = [str(c).strip() for c in raw.iloc[header_row]]
    columns = [normalize_column(c) for c in original]
    df = raw.iloc[header_row + 1:].copy()
    df.columns = columns
    return df, original, columns


def check_file(path: Path) -> dict:
    """Check one .xlsx file and return a JSON-ready result dict."""
    result = {"file": path.name, "status": "ok", "issues": []}

    sheets = read_sheets(path)
    table = locate_table(sheets)
    if table is None:
        result["status"] = "error"
        result["issues"].append("header row not found on any sheet")
        return result
    sheet, raw, header_row = table

    df, original, columns = extract_table(raw, header_row)
    rows_before = len(df)
    df = df.dropna(how="all")  # drop rows where all cells are empty

    missing = [c for c in REQUIRED_COLUMNS if c not in columns]
    extra = [c for c in columns if c not in REQUIRED_COLUMNS]
    # Report only real renames (aliases), not case changes like "Date" -> "date"
    renamed = {o: n for o, n in zip(original, columns) if o.lower() != n}

    # Numeric check: values that can't be converted to a number as they are
    bad_values = {}
    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            numbers = pd.to_numeric(df[col], errors="coerce")
            bad = int((numbers.isna() & df[col].notna()).sum())
            if bad:
                bad_values[col] = bad

    result.update({
        "sheet": sheet,
        "header_row": header_row + 1,          # 1-based, like in Excel
        "data_rows": len(df),
        "empty_rows_dropped": rows_before - len(df),
        "missing_columns": missing,
        "extra_columns": extra,
        "renamed_columns": renamed,
        "non_numeric_values": bad_values,
    })

    # Severity: missing columns or no data break the import; the rest needs attention
    if missing:
        result["status"] = "error"
        result["issues"].append(f"missing columns: {', '.join(missing)}")
    if len(df) == 0:
        result["status"] = "error"
        result["issues"].append("no data rows")
    if sheet != next(iter(sheets)):  # dicts keep the sheet order of the workbook
        result["issues"].append(f"data is on sheet '{sheet}', not the first one")
    if header_row != 0:
        result["issues"].append(f"header is on row {header_row + 1}, not 1")
    if renamed:
        result["issues"].append(f"renamed columns: {renamed}")
    if extra:
        result["issues"].append(f"extra columns: {', '.join(extra)}")
    if bad_values:
        result["issues"].append(f"non-numeric values: {bad_values}")
    if result["status"] == "ok" and result["issues"]:
        result["status"] = "warning"

    return result