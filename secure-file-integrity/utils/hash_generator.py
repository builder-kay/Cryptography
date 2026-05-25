"""Utilities for generating cryptographic file hashes."""

import hashlib
from pathlib import Path


def generate_sha256(file_path: Path) -> str:
    """Generate the SHA-256 hash for a file using chunked reads."""
    sha256 = hashlib.sha256()

    with Path(file_path).open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()
