"""Mask secrets and personal data before pasting text into an AI tool."""
import re
import sys
from collections import Counter


def valid_tckn(s: str) -> bool:
    """Turkish national ID checksum: 11 digits, first not 0, digits 10 and 11 are check digits."""
    d = [int(c) for c in s]
    if len(d) != 11 or d[0] == 0:
        return False
    if ((sum(d[0:9:2]) * 7 - sum(d[1:8:2])) % 10) != d[9]:
        return False
    return sum(d[:10]) % 10 == d[10]


RULES = [
    ("bearer token", re.compile(r"(?i)(bearer\s+)[A-Za-z0-9\-._~+/]+=*"), r"\1***"),
    ("secret value", re.compile(r"(?i)\b(password|pwd|secret|api[_-]?key|token)(\s*[=:]\s*)(\"[^\"]*\"|'[^']*'|[^;\s]+)"), r"\1\2***"),
    ("aws access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AKIA****************"),
    ("email", re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"), "<email>"),
    ("iban", re.compile(r"\bTR\d{2}(?:\s?\d{4}){5}\s?\d{2}\b"), "<iban>"),
    ("phone", re.compile(r"(?:\+90|0)\s?5\d{2}\s?\d{3}\s?\d{2}\s?\d{2}\b"), "<phone>"),
]


def mask(text: str) -> tuple[str, Counter]:
    counts = Counter()
    for name, pattern, repl in RULES:
        text, n = pattern.subn(repl, text)
        counts[name] += n

    def tckn(m):
        if valid_tckn(m.group()):
            counts["tckn"] += 1
            return "<tckn>"
        return m.group()

    text = re.sub(r"\b\d{11}\b", tckn, text)
    return text, +counts


if __name__ == "__main__":
    raw = open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1 else sys.stdin.read()
    masked, counts = mask(raw)
    print(masked)
    print("--- masked:", ", ".join(f"{k} x{v}" for k, v in counts.items()) or "nothing", file=sys.stderr)
