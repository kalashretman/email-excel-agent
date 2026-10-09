"""Generate 10 fake Excel reports: one clean template and 9 typical real-world problems."""

from datetime import datetime

from openpyxl import Workbook

from config import BASE_DIR

TEST_DIR = BASE_DIR / "test_files"

# The "standard" template every partner is supposed to use
HEADER = ["date", "city", "product", "quantity", "price"]


def save(filename: str, sheets: dict[str, list[list]]) -> None:
    """Write a workbook: {sheet name: rows}, one list = one Excel row."""
    wb = Workbook()
    wb.remove(wb.active)  # drop the default empty sheet
    for title, rows in sheets.items():
        ws = wb.create_sheet(title)
        for row in rows:
            ws.append(row)
    wb.save(TEST_DIR / filename)
    print(f"created {filename}")


def main() -> None:
    TEST_DIR.mkdir(exist_ok=True)

    # 1. Clean: exactly the standard template
    save("report_kyiv_2026-09-30.xlsx", {"Sheet1": [
        HEADER,
        ["2026-09-30", "Kyiv", "Widget A", 10, 125.50],
        ["2026-09-30", "Kyiv", "Widget B", 4, 89.90],
        ["2026-09-30", "Kyiv", "Widget C", 25, 12.00],
    ]})

    # 2. Columns in a different order plus an extra column
    save("report_lviv_2026-09-30.xlsx", {"Sheet1": [
        ["city", "date", "price", "quantity", "product", "comment"],
        ["Lviv", "2026-09-30", 125.50, 7, "Widget A", None],
        ["Lviv", "2026-09-30", 89.90, 2, "Widget B", "urgent"],
    ]})

    # 3. Title rows above the header, renamed columns, empty row, "n/a" in numbers
    save("report_odesa_2026-10-01.xlsx", {"Sheet1": [
        ["Sales report"],
        ["Partner B, Odesa branch"],
        [],
        ["Date", " City ", "Product", "Qty", "Price, UAH"],
        ["2026-10-01", "Odesa", "Widget A", 3, 125.50],
        [],
        ["2026-10-01", "Odesa", "Widget B", "n/a", 89.90],
    ]})

    # 4. A required column is missing (no price)
    save("report_dnipro_2026-10-01.xlsx", {"Sheet1": [
        ["date", "city", "product", "quantity"],
        ["2026-10-01", "Dnipro", "Widget A", 12],
    ]})

    # 5. Ukrainian headers and dates as DD.MM.YYYY text
    save("report_kharkiv_2026-10-02.xlsx", {"Аркуш1": [
        ["Дата", "Місто", "Товар", "Кількість", "Ціна"],
        ["02.10.2026", "Харків", "Widget A", 6, 125.50],
        ["02.10.2026", "Харків", "Widget C", 40, 12.00],
    ]})

    # 6. Real Excel dates + numbers typed as text with comma decimals and spaces
    save("report_zaporizhzhia_2026-10-02.xlsx", {"Sheet1": [
        HEADER,
        [datetime(2026, 10, 2), "Zaporizhzhia", "Widget A", "1 250", "125,50"],
        [datetime(2026, 10, 2), "Zaporizhzhia", "Widget B", "15", "89,9"],
    ]})

    # 7. A "Total" row at the bottom that must not be imported as data
    save("report_poltava_2026-10-03.xlsx", {"Sheet1": [
        HEADER,
        ["2026-10-03", "Poltava", "Widget A", 5, 125.50],
        ["2026-10-03", "Poltava", "Widget B", 8, 89.90],
        [],
        ["Разом", None, None, 13, None],
    ]})

    # 8. Data is on the SECOND sheet; the first one is just notes
    save("report_vinnytsia_2026-10-03.xlsx", {
        "Info": [["Prepared by: sales team"], ["Questions: see the Data sheet"]],
        "Data": [
            HEADER,
            ["2026-10-03", "Vinnytsia", "Widget C", 30, 12.00],
        ],
    })

    # 9. A completely different template: no known column names at all
    #    (later the LLM will map these columns, week 4)
    save("report_chernihiv_2026-10-04.xlsx", {"Sheet1": [
        ["Дата відвантаження", "Філія", "Найменування позиції", "К-сть, шт", "Вартість за од."],
        ["04.10.2026", "Чернігів", "Widget A", 9, 125.50],
    ]})

    # 10. Valid header but no data rows
    save("report_sumy_2026-10-04.xlsx", {"Sheet1": [HEADER]})


if __name__ == "__main__":
    main()