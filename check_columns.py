"""Week 1 mini-project: check every .xlsx in test_files/ and write a JSON report."""

from collections import Counter
from datetime import datetime

from config import BASE_DIR, OUTPUT_DIR
from excel_checker import check_file
from storage import save_json

TEST_DIR = BASE_DIR / "test_files"
REPORT_FILE = OUTPUT_DIR / "columns_report.json"


def list_excel_files(folder) -> list:
    """All .xlsx files in a folder, except Excel lock files like '~$report.xlsx'."""
    return [p for p in sorted(folder.glob("*.xlsx")) if not p.name.startswith("~$")]


def safe_check(path) -> dict:
    """Run check_file, but turn an unreadable file into an 'error' result."""
    try:
        return check_file(path)
    except Exception as e:
        # One broken attachment must not stop the whole run
        return {"file": path.name, "status": "error", "issues": [f"cannot read file: {e}"]}


def main() -> None:
    results = [safe_check(path) for path in list_excel_files(TEST_DIR)]

    for r in results:
        print(f"{r['status'].upper():<8}| {r['file']}")
        for issue in r["issues"]:
            print(f"        - {issue}")

    summary = dict(Counter(r["status"] for r in results))
    save_json(REPORT_FILE, {
        "checked_at": datetime.now().isoformat(timespec="seconds"),
        "summary": summary,
        "files": results,
    })

    print()
    print(f"summary: {summary}")
    print(f"report:  {REPORT_FILE.name}")


if __name__ == "__main__":
    main()