"""Day 11: clean every test report and save the result as CSV."""

from config import BASE_DIR, OUTPUT_DIR
from excel_cleaner import load_report

TEST_DIR = BASE_DIR / "test_files"
CLEAN_DIR = OUTPUT_DIR / "clean"


def main() -> None:
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    for path in sorted(TEST_DIR.glob("*.xlsx")):
        if path.name.startswith("~$"):
            continue  # skip Excel lock files
        df, notes = load_report(path)
        print(f"=== {path.name}  ({len(df)} rows) {'; '.join(notes)}")
        if not df.empty:
            print(df.to_string(index=False))
            # utf-8-sig: Excel opens Cyrillic CSV correctly with this encoding
            df.to_csv(CLEAN_DIR / f"{path.stem}.csv", index=False, encoding="utf-8-sig")
        print()


if __name__ == "__main__":
    main()