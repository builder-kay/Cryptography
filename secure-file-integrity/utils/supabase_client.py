"""Supabase database client helpers for file integrity records."""

import os
from functools import lru_cache

from dotenv import load_dotenv
from supabase import create_client


load_dotenv()


class SupabaseConfigurationError(RuntimeError):
    """Raised when Supabase credentials are missing from environment variables."""


@lru_cache(maxsize=1)
def get_supabase_client():
    """Create and cache a Supabase client from protected environment variables."""
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        raise SupabaseConfigurationError(
            "Supabase credentials are missing. Add SUPABASE_URL and SUPABASE_KEY to .env."
        )

    return create_client(supabase_url, supabase_key)


def insert_file_record(filename: str, sha256_hash: str, verification_status: str) -> dict:
    """Insert a new file hash record into the files table."""
    client = get_supabase_client()
    response = (
        client.table("files")
        .insert(
            {
                "filename": filename,
                "sha256_hash": sha256_hash,
                "verification_status": verification_status,
            }
        )
        .execute()
    )
    return response.data[0] if response.data else {}


def get_file_by_filename(filename: str) -> dict | None:
    """Fetch the newest file record matching a secured filename."""
    client = get_supabase_client()
    response = (
        client.table("files")
        .select("*")
        .eq("filename", filename)
        .order("upload_timestamp", desc=True)
        .limit(1)
        .execute()
    )
    return response.data[0] if response.data else None


def get_files() -> list[dict]:
    """Fetch all file integrity records for the dashboard."""
    client = get_supabase_client()
    response = (
        client.table("files")
        .select("*")
        .order("upload_timestamp", desc=True)
        .execute()
    )
    return response.data or []


def update_verification_status(record_id: str, verification_status: str) -> dict:
    """Update a record after an integrity verification check."""
    client = get_supabase_client()
    response = (
        client.table("files")
        .update({"verification_status": verification_status})
        .eq("id", record_id)
        .execute()
    )
    return response.data[0] if response.data else {}
