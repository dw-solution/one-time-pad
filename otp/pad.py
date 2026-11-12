"""Pad generation backed by the operating system's CSPRNG.

`secrets` draws from os.urandom (getrandom on Linux, BCryptGenRandom on
Windows, the kernel CSPRNG on macOS). `secrets.choice` uses rejection
sampling, so every symbol is equally likely with no modulo bias.
"""

import secrets
import string
from datetime import datetime, timezone

ALPHABETS = {
    "Digits (0-9)": string.digits,
    "Letters (A-Z)": string.ascii_uppercase,
    "Hex (0-9, A-F)": string.digits + "ABCDEF",
}

DEFAULT_ALPHABET = "Digits (0-9)"


def generate_symbols(count, alphabet=string.digits):
    if count < 1:
        raise ValueError("count must be at least 1")
    if len(set(alphabet)) < 2:
        raise ValueError("alphabet needs at least two distinct symbols")
    return "".join(secrets.choice(alphabet) for _ in range(count))


def format_groups(symbols, group_size=5, groups_per_line=10):
    groups = [symbols[i:i + group_size] for i in range(0, len(symbols), group_size)]
    lines = [" ".join(groups[i:i + groups_per_line])
             for i in range(0, len(groups), groups_per_line)]
    return "\n".join(lines)


def generate_pad(groups=50, group_size=5, alphabet=string.digits, groups_per_line=10):
    symbols = generate_symbols(groups * group_size, alphabet)
    return format_groups(symbols, group_size, groups_per_line)


def pad_id():
    return secrets.token_hex(4).upper()


def pad_header(identifier, alphabet_name, groups, group_size):
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    return (f"PAD {identifier}  {stamp}\n"
            f"{alphabet_name}, {groups} groups of {group_size}")
