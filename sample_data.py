"""Fake inbox for development. Real IMAP data will replace it in week 3."""

EMAILS: list[dict] = [
    {"message_id": "<001@mail>", "from": "reports@partner-a.example",
     "subject": "Report 2026-09-30 Kyiv", "attachments": ["kyiv_2026-09-30.xlsx"]},
    {"message_id": "<002@mail>", "from": "Reports@Partner-B.example",
     "subject": "report 2026-09-30 Lviv", "attachments": ["LVIV.XLSX"]},
    {"message_id": "<003@mail>", "from": "news@shop.example",
     "subject": "Weekly deals", "attachments": []},
    {"message_id": "<004@mail>", "from": "reports@partner-a.example",
     "subject": "Invoice 2026-09-30", "attachments": ["invoice.pdf"]},
    {"message_id": "<005@mail>", "from": "reports@partner-a.example",
     "subject": "Report 2026-10-01 Odesa", "attachments": []},
    {"message_id": "<006@mail>", "from": "reports@partner-b.example",
     "subject": "Report 2026-10-01 Dnipro", "attachments": ["photo.jpg", "data.csv"]},
    {"message_id": "<007@mail>", "from": "reports@partner-a.example",
     "subject": "Report 2026-09-29 Kyiv", "attachments": ["kyiv_2026-09-29.xlsx"]},
    {"message_id": "<008@mail>", "from": "reports@partner-a.example.evil.com",
     "subject": "Report 2026-10-01 Kyiv", "attachments": ["kyiv.xlsx"]},
    {"message_id": "<009@mail>", "from": "Partner A <reports@partner-a.example>",
     "subject": "Report 2026-10-02 Kharkiv", "attachments": ["kharkiv.xlsx"]},
    {"message_id": "<010@mail>", "from": "reports@partner-b.example",
     "subject": "Report 30.09.2026 Lviv", "attachments": ["lviv.xlsx"]},
]