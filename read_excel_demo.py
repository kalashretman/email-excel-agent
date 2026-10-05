"""Open every test Excel file with pandas and show what it really looks like."""

import pandas as pd

from config import BASE_DIR

TEST_DIR = BASE_DIR / "test_files"


def describe(path) -> None:
    """Print the shape, column names, column types and first rows of one file."""
    # header=0: pandas assumes the FIRST row holds column names
    df = pd.read_excel(path, header=0)

    print(f"=== {path.name}")
    print(f"rows x cols: {df.shape}")
    print(f"columns:     {list(df.columns)}")
    print(f"dtypes:      {dict(df.dtypes.astype(str))}")
    print(df.head().to_string())
    print()


def main() -> None:
    # sorted() makes the order the same on macOS and Windows
    for path in sorted(TEST_DIR.glob("*.xlsx")):
        describe(path)


if __name__ == "__main__":
    main()