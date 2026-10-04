from email.utils import parseaddr

# Only emails from these sender domains are accepted (exact match, lowercase)
ALLOWED_DOMAINS = {"partner-a.example", "partner-b.example"}

# Message-IDs that were already saved to the DB (later: processed_emails table)
PROCESSED_IDS = {"<007@mail>"}

# Fake inbox: each email is a dict, the same shape IMAP data will have later
emails = [
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
]

def get_domain(sender: str) -> str:
    """Return the lowercase domain of a sender, e.g. 'Name <a@B.com>' -> 'b.com'."""
    # parseaddr handles both "a@b.com" and "Name <a@b.com>" formats
    _, address = parseaddr(sender)
    # Everything after the LAST "@" is the domain
    return address.rpartition("@")[2].lower()

def has_xlsx(attachments: list[str]) -> bool:
    """True if at least one attachment is an .xlsx file (case-insensitive)."""
    return any(name.lower().endswith(".xlsx") for name in attachments)

def check_email(email: dict, processed_ids: set[str]) -> str | None:
    """Return None if the email passes all rules, else the first failed rule code."""
    # 1. Idempotency first: never process the same email twice
    if email["message_id"] in processed_ids:
        return "already_processed"

    # 2. Exact domain match: "partner-a.example.evil.com" must NOT pass
    if get_domain(email["from"]) not in ALLOWED_DOMAINS:
        return "unknown_sender"

    # 3. Subject must look like a report
    if not email["subject"].strip().lower().startswith("report"):
        return "bad_subject"

    # 4. We only care about emails with Excel attachments
    if not has_xlsx(email["attachments"]):
        return "no_xlsx"

    return None


if __name__ == "__main__":
    accepted = []
    reasons = {}

    for email in emails:
        reason = check_email(email, PROCESSED_IDS)
        if reason is None:
            accepted.append(email)
            print(f"ACCEPT | {email['message_id']} | {email['subject']}")
        else:
            # Count how many emails were skipped for each reason
            reasons[reason] = reasons.get(reason, 0) + 1
            print(f"SKIP   | {email['message_id']} | {reason}")

    print()
    print(f"accepted: {len(accepted)}")
    print(f"skipped:  {sum(reasons.values())}")
    print(f"reasons:  {reasons}")