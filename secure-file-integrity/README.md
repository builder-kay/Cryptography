# TrueForm: Secure File Integrity Verification System Using SHA-256

## Project Overview

This full-stack web application verifies whether uploaded files have been changed after their original upload. It generates a SHA-256 cryptographic hash for each file, stores the trusted hash in a Supabase PostgreSQL database, and later compares new uploads against the stored baseline.

## Real-World Problem Statement

Organizations exchange documents, reports, backups, certificates, logs, and software packages every day. If one of those files is modified by accident or tampered with by an attacker, users need a reliable way to detect the change. File integrity verification solves this by storing a trusted fingerprint of a file and comparing it with future versions.

## Objectives

- Upload files through a clean web interface.
- Generate SHA-256 hashes using Python `hashlib`.
- Store file metadata and hashes in Supabase PostgreSQL.
- Verify later uploads against stored baseline hashes.
- Show clear authentic or tampered status messages.
- Provide a dashboard of uploaded files and verification results.
- Demonstrate secure upload handling for a cryptography project.

## Features

- Modern cybersecurity-themed responsive UI.
- File upload and temporary server-side storage.
- SHA-256 hash generation.
- Supabase PostgreSQL integration with `supabase-py`.
- File integrity verification workflow.
- Dashboard table for stored records.
- Green and red status indicators.
- File size validation with a 16 MB limit.
- Secure filename handling using Werkzeug.
- Path traversal prevention through generated temporary filenames.
- Duplicate filename detection.
- Clear error handling for invalid uploads and database setup issues.

## Technologies Used

| Layer | Technology |
| --- | --- |
| Frontend | HTML, CSS, JavaScript |
| Backend | Python Flask |
| Database | Supabase PostgreSQL |
| Cryptography | `hashlib` SHA-256 |
| Environment Config | `python-dotenv` |
| Upload Security | Werkzeug `secure_filename` |

## Explanation of SHA-256

SHA-256 is a cryptographic hash function from the SHA-2 family. It converts input data of any size into a fixed 256-bit output, commonly displayed as a 64-character hexadecimal string.

Important properties:

- Deterministic: the same file always produces the same hash.
- Collision resistant: it is computationally difficult to find two different files with the same hash.
- Avalanche effect: even a tiny file change creates a very different hash.
- One-way: the original file cannot be reconstructed from the hash.

Example:

```text
Input: cryptography
SHA-256: 09137d42f0c76f2617a52df1ba24e1cdf7b7f965048df023d9129a6811f3a12b
```

## Supabase Integration Explanation

Supabase provides a hosted PostgreSQL database. This project uses the `supabase-py` SDK to insert, fetch, and update records in a table named `files`.

The application loads credentials from `.env`:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_or_service_role_key
FLASK_SECRET_KEY=replace-this-with-a-random-secret
```

The credentials are not hardcoded in Python files. This protects secrets and makes the project easier to deploy in different environments.

## System Architecture

```text
+-------------+        +--------------+        +-------------------+
|   Browser   | -----> | Flask Server | -----> | Supabase Database |
| HTML/CSS/JS |        | Python API   |        | PostgreSQL files  |
+-------------+        +--------------+        +-------------------+
       |                       |
       | Upload file           | hashlib.sha256()
       |                       |
       +-----------------------+
```

## Upload Flowchart

```text
User selects file
       |
       v
Flask validates upload
       |
       v
Save temporarily in uploads/
       |
       v
Generate SHA-256 hash
       |
       v
Check duplicate filename
       |
       v
Store metadata in Supabase
       |
       v
Display generated hash
```

## Verification Flowchart

```text
User uploads file again
       |
       v
Generate new SHA-256 hash
       |
       v
Fetch stored hash by filename
       |
       v
Compare hashes
       |
       +-------------------+
       |                   |
       v                   v
Hashes match         Hashes differ
       |                   |
       v                   v
File is Authentic    WARNING: File Has Been Modified
```

## Database Schema

Create a table called `files` in Supabase:

```sql
create table files (
    id uuid primary key default gen_random_uuid(),
    filename text not null,
    sha256_hash text not null,
    verification_status text not null,
    upload_timestamp timestamp default now()
);
```

The same SQL is also available in `database/schema.sql`.

Recommended duplicate protection:

```sql
create unique index files_filename_unique on files (filename);
```

## Folder Structure

```text
secure-file-integrity/
|
├── app.py
├── requirements.txt
├── .env
|
├── templates/
│   ├── index.html
│   ├── dashboard.html
|
├── static/
│   ├── style.css
│   ├── script.js
|
├── uploads/
|
├── utils/
│   ├── hash_generator.py
│   ├── supabase_client.py
│   ├── verifier.py
|
└── README.md
```

## Installation Guide

1. Open a terminal in the project folder.

```bash
cd secure-file-integrity
```

2. Create and activate a virtual environment.

```bash
python -m venv venv
venv\Scripts\activate
```

On macOS or Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies.

```bash
pip install -r requirements.txt
```

## Environment Variable Setup

Update `.env` with your Supabase project values:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-api-key
FLASK_SECRET_KEY=your-random-flask-secret
```

For classroom demos, the anon key can be used if table policies allow the required operations. For server-side production apps, prefer a service role key stored securely on the server only.

## Supabase Setup Instructions

1. Create a Supabase account.
2. Create a new project.
3. Open the SQL Editor.
4. Run the database schema SQL from this README.
5. Go to Project Settings.
6. Copy the Project URL into `SUPABASE_URL`.
7. Copy the API key into `SUPABASE_KEY`.
8. Configure Row Level Security policies if using the anon key.

Example development policy:

```sql
alter table files enable row level security;

create policy "Allow file integrity demo access"
on files
for all
using (true)
with check (true);
```

## Running the Project

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Usage Workflow

1. Open the home page.
2. Upload an original file in the baseline upload form.
3. Copy or review the generated SHA-256 hash.
4. Open the dashboard to confirm the record was stored.
5. Upload the same file in the verification form.
6. Review the integrity result.
7. Modify the file contents and upload it again with the same filename.
8. Confirm the warning status appears.

## Example Verification Outputs

Authentic file:

```text
File is Authentic
New Upload Hash: 4f8b42c2c7f1e85f5c6b3f5d2d836c0d7f9ad50c12ef2a6b4af8a9c62d725f71
Stored Hash:     4f8b42c2c7f1e85f5c6b3f5d2d836c0d7f9ad50c12ef2a6b4af8a9c62d725f71
```

Tampered file:

```text
WARNING: File Has Been Modified
New Upload Hash: 84a9c7f0ec2b89da31622b8d8f0a8f53cb10a712d761f83d099f7a114c8f5a43
Stored Hash:     4f8b42c2c7f1e85f5c6b3f5d2d836c0d7f9ad50c12ef2a6b4af8a9c62d725f71
```

## Security Concepts Used

- Cryptographic hashing with SHA-256.
- Baseline hash storage.
- File integrity comparison.
- Secure filename normalization.
- File size validation.
- Environment-based secret management.
- Constant-time hash comparison with `hmac.compare_digest`.
- Duplicate filename handling.
- Database exception handling.

## Screenshots Placeholder

Add screenshots here after running the project:

```text
screenshots/home-page.png
screenshots/hash-result.png
screenshots/dashboard.png
screenshots/tampered-warning.png
```

## Future Improvements

- Add user authentication.
- Store files in Supabase Storage instead of temporary local storage.
- Add audit logs for every verification attempt.
- Support multiple baseline versions per filename.
- Add drag-and-drop upload.
- Add CSV export for dashboard records.
- Deploy to a cloud platform.
- Add automated tests.

## Team Members Section

| Name | Role |
| --- | --- |
| Team Member 1 | Backend and Supabase Integration |
| Team Member 2 | Frontend UI and Dashboard |
| Team Member 3 | Cryptography Research and Documentation |

## License

This project is provided for educational use. You may adapt it for academic presentations, demos, and learning projects.

## Conclusion

The Secure File Integrity Verification System demonstrates how cryptographic hashing can protect trust in digital files. By combining Flask, SHA-256, and Supabase PostgreSQL, the project provides a practical example of detecting file modification and presenting integrity status in a real-world cybersecurity interface.
