"""Entry point: filter the inbox, remember processed emails, save a JSON report."""

from collections import Counter

from config import PROCESSED_IDS_FILE, RUN_REPORT_FILE
from filters import check_email
from sample_data import EMAILS
from storage import load_processed_ids, save_processed_ids, save_run_report
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
    processed_ids = load_processed_ids(PROCESSED_IDS_FILE)
    accepted, skipped = run(EMAILS, processed_ids)

    for item in accepted:
        print(f"ACCEPT | {item['message_id']} | {item['date']} | {item['city']}")
    for message_id, reason in skipped:
        print(f"SKIP   | {message_id} | {reason}")

    # For now "processed" = accepted. From week 3: only after a successful DB write.
    processed_ids |= {item["message_id"] for item in accepted}
    save_processed_ids(PROCESSED_IDS_FILE, processed_ids)
    save_run_report(RUN_REPORT_FILE, accepted, skipped)

    reasons = Counter(reason for _, reason in skipped)
    print()
    print(f"accepted: {len(accepted)} | skipped: {len(skipped)} | reasons: {dict(reasons)}")
    print(f"state:  {PROCESSED_IDS_FILE.name} ({len(processed_ids)} ids)")
    print(f"report: {RUN_REPORT_FILE.name}")


if __name__ == "__main__":
    main()