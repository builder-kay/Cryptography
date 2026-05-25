"""Flask application for SHA-256 based file integrity verification."""

import os
from pathlib import Path
from uuid import uuid4

from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from utils.hash_generator import generate_sha256
from utils.supabase_client import (
    SupabaseConfigurationError,
    get_file_by_filename,
    get_files,
    insert_file_record,
    update_verification_status,
)
from utils.verifier import compare_hashes


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
MAX_FILE_SIZE = 16 * 1024 * 1024

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_DIR
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "development-secret-key")


def allowed_upload(file_storage) -> tuple[bool, str]:
    """Validate that a request contains a usable uploaded file."""
    if not file_storage:
        return False, "No file was uploaded."

    if not file_storage.filename:
        return False, "Please choose a file before submitting."

    safe_name = secure_filename(file_storage.filename)
    if not safe_name:
        return False, "The filename is invalid."

    return True, safe_name


def save_temporary_upload(file_storage, safe_name: str) -> Path:
    """Save an uploaded file with a collision-resistant temporary name."""
    UPLOAD_DIR.mkdir(exist_ok=True)
    destination = UPLOAD_DIR / f"{uuid4()}_{safe_name}"
    file_storage.save(destination)
    return destination


@app.errorhandler(413)
def file_too_large(_error):
    """Return a friendly message when users exceed the upload limit."""
    flash("File is too large. Maximum allowed size is 16 MB.", "error")
    return redirect(url_for("home"))


@app.route("/")
def home():
    """Render the home page with upload and verification forms."""
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    """Upload a file, generate its SHA-256 hash, and store metadata."""
    file_storage = request.files.get("file")
    is_valid, result = allowed_upload(file_storage)

    if not is_valid:
        flash(result, "error")
        return redirect(url_for("home"))

    safe_name = result
    upload_path = save_temporary_upload(file_storage, safe_name)

    try:
        file_hash = generate_sha256(upload_path)
        existing_record = get_file_by_filename(safe_name)

        if existing_record:
            flash(
                "A record already exists for this filename. Use verification to check integrity.",
                "warning",
            )
        else:
            insert_file_record(
                filename=safe_name,
                sha256_hash=file_hash,
                verification_status="Original Uploaded",
            )
            flash("File uploaded and hash stored successfully.", "success")

        return render_template(
            "index.html",
            generated_hash=file_hash,
            uploaded_filename=safe_name,
            upload_mode=True,
        )
    except SupabaseConfigurationError as error:
        flash(str(error), "error")
    except Exception as error:
        flash(f"Upload failed: {error}", "error")

    return redirect(url_for("home"))


@app.route("/verify", methods=["POST"])
def verify_file():
    """Compare a newly uploaded file hash against the stored Supabase hash."""
    file_storage = request.files.get("file")
    is_valid, result = allowed_upload(file_storage)

    if not is_valid:
        flash(result, "error")
        return redirect(url_for("home"))

    safe_name = result
    upload_path = save_temporary_upload(file_storage, safe_name)

    try:
        new_hash = generate_sha256(upload_path)
        stored_record = get_file_by_filename(safe_name)

        if not stored_record:
            flash("No stored baseline hash exists for this filename.", "error")
            return render_template(
                "index.html",
                verification_result="No Stored Record",
                verification_hash=new_hash,
                uploaded_filename=safe_name,
            )

        stored_hash = stored_record["sha256_hash"]
        is_authentic = compare_hashes(new_hash, stored_hash)
        status = "File is Authentic" if is_authentic else "WARNING: File Has Been Modified"
        update_verification_status(stored_record["id"], status)

        return render_template(
            "index.html",
            verification_result=status,
            verification_hash=new_hash,
            stored_hash=stored_hash,
            uploaded_filename=safe_name,
            is_authentic=is_authentic,
        )
    except SupabaseConfigurationError as error:
        flash(str(error), "error")
    except Exception as error:
        flash(f"Verification failed: {error}", "error")

    return redirect(url_for("home"))


@app.route("/dashboard")
def dashboard():
    """Display all file integrity records stored in Supabase."""
    try:
        files = get_files()
        return render_template("dashboard.html", files=files)
    except SupabaseConfigurationError as error:
        flash(str(error), "error")
    except Exception as error:
        flash(f"Could not load dashboard records: {error}", "error")

    return render_template("dashboard.html", files=[])


if __name__ == "__main__":
    app.run(debug=True)
