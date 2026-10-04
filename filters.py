"""Rules that decide whether an email should be processed by the agent."""

from email.utils import parseaddr

from config import ALLOWED_DOMAINS, ALLOWED_EXTENSIONS
from subject_parser import parse_subject


def get_domain(sender: str) -> str:
    """Return the lowercase domain of a sender, e.g. 'Name <a@B.com>' -> 'b.com'."""
    # parseaddr handles both "a@b.com" and "Name <a@b.com>" formats
    _, address = parseaddr(sender)
    # Everything after the LAST "@" is the domain
    return address.rpartition("@")[2].lower()


def has_allowed_attachment(attachments: list[str]) -> bool:
    """True if at least one attachment has an allowed extension (case-insensitive)."""
    # str.endswith() accepts a tuple: matches any of the extensions
    return any(name.lower().endswith(ALLOWED_EXTENSIONS) for name in attachments)


def check_email(email: dict, processed_ids: set[str]) -> str | None:
    """Return None if the email passes all rules, else the first failed rule code."""
    # 1. Idempotency first: never process the same email twice
    if email["message_id"] in processed_ids:
        return "already_processed"

    # 2. Exact domain match: "partner-a.example.evil.com" must NOT pass
    if get_domain(email["from"]) not in ALLOWED_DOMAINS:
        return "unknown_sender"

    # 3. Subject must be a valid report subject (reuses the Day 2 parser)
    if parse_subject(email["subject"]) is None:
        return "bad_subject"

    # 4. We only care about emails with Excel attachments
    if not has_allowed_attachment(email["attachments"]):
        return "no_xlsx"

    return None