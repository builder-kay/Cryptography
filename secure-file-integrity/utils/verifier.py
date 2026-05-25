"""Integrity verification helpers."""

import hmac


def compare_hashes(new_hash: str, stored_hash: str) -> bool:
    """Compare two SHA-256 hashes using constant-time comparison."""
    return hmac.compare_digest(new_hash, stored_hash)
