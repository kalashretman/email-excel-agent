"""Generate fake Excel reports for development: clean ones and messy ones."""

from openpyxl import Workbook

from config import BASE_DIR

TEST_DIR = BASE_DIR / "test_files"

# The "standard" template every partner is supposed to use
HEADER = ["date", "city", "product", "quantity", "price"]
ROWS = [
    ["2026-09-30", "Kyiv", "Widget A", 10, 125.50],
    ["2026-09-30", "Kyiv", "Widget B", 4, 89.90],
    ["2026-09-30", "Kyiv", "Widget C", 25, 12.00],
]


def save(filename: str, rows: list[list]) -> None:
    """Write rows to a new .xlsx file, one list = one Excel row."""
    wb = Workbook()
    ws = wb.active
    for row in rows:
        ws.append(row)
    wb.save(TEST_DIR / filename)
    print(f"created {filename}")


def main() -> None:
    TEST_DIR.mkdir(exist_ok=True)

    # 1. Clean: exactly the standard template
    save("report_kyiv_2026-09-30.xlsx", [HEADER, *ROWS])

    # 2. Same data, but columns in a different order plus an extra column
    save("report_lviv_2026-09-30.xlsx", [
        ["city", "date", "price", "quantity", "product", "comment"],
        ["Lviv", "2026-09-30", 125.50, 7, "Widget A", ""],
        ["Lviv", "2026-09-30", 89.90, 2, "Widget B", "urgent"],
    ])

    # 3. Messy: title rows above the header, renamed columns,
    #    an empty row in the data and text in a numeric column
    save("report_odesa_2026-10-01.xlsx", [
        ["Sales report"],
        ["Partner B, Odesa branch"],
        [],
        ["Date", " City ", "Product", "Qty", "Price, UAH"],
        ["2026-10-01", "Odesa", "Widget A", 3, 125.50],
        [],
        ["2026-10-01", "Odesa", "Widget B", "n/a", 89.90],
    ])

    # 4. Missing a required column (no price)
    save("report_dnipro_2026-10-01.xlsx", [
        ["date", "city", "product", "quantity"],
        ["2026-10-01", "Dnipro", "Widget A", 12],
    ])


if __name__ == "__main__":
    main()