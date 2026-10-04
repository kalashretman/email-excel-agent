"""Entry point: run the email filter over the inbox and print a summary."""

from collections import Counter

from filters import check_email
from sample_data import EMAILS, PROCESSED_IDS
from subject_parser import parse_subject


def run(emails: list[dict], processed_ids: set[str]) -> tuple[list[dict], list[tuple[str, str]]]:
    """Split emails into accepted (with parsed date/city) and skipped (id, reason)."""
    accepted: list[dict] = []
    skipped: list[tuple[str, str]] = []

    for email in emails:
        reason = check_email(email, processed_ids)
        if reason is None:
            # Merge the email with its parsed subject: {..., "date": ..., "city": ...}
            accepted.append({**email, **parse_subject(email["subject"])})
        else:
            skipped.append((email["message_id"], reason))

    return accepted, skipped


def main() -> None:
    accepted, skipped = run(EMAILS, PROCESSED_IDS)

    for item in accepted:
        print(f"ACCEPT | {item['message_id']} | {item['date']} | {item['city']}")
    for message_id, reason in skipped:
        print(f"SKIP   | {message_id} | {reason}")

    # Counter counts how many times each reason appears
    reasons = Counter(reason for _, reason in skipped)

    print()
    print(f"accepted: {len(accepted)}")
    print(f"skipped:  {len(skipped)}")
    print(f"reasons:  {dict(reasons)}")


if __name__ == "__main__":
    main()