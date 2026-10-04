"""Project settings. Later the secrets part will move to .env (Day 5)."""

# Only emails from these sender domains are accepted (exact match, lowercase)
ALLOWED_DOMAINS: set[str] = {"partner-a.example", "partner-b.example"}

# Only these attachment types are processed
ALLOWED_EXTENSIONS: tuple[str, ...] = (".xlsx",)