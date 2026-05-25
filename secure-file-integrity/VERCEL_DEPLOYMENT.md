# Deploying TrueForm to Vercel

## Current Folder Structure

Deploy from this folder:

```text
secure-file-integrity/
|
├── app.py
├── requirements.txt
├── vercel.json
├── .vercelignore
|
├── templates/
│   ├── index.html
│   ├── dashboard.html
|
├── static/
│   ├── style.css
│   ├── script.js
|
├── utils/
│   ├── hash_generator.py
│   ├── supabase_client.py
│   ├── verifier.py
|
├── database/
│   ├── schema.sql
|
└── README.md
```

Do not upload `venv/`, `.env`, `uploads/`, or `__pycache__/`.

## 1. Prepare Supabase

Open Supabase SQL Editor and run:

```text
database/schema.sql
```

This creates the `files` table and demo Row Level Security policies.

## 2. Create a Git Repository

From inside `secure-file-integrity/`:

```bash
git init
git add .
git commit -m "Deploy TrueForm Flask app"
```

Push the repository to GitHub, GitLab, or Bitbucket.

## 3. Import Project on Vercel

1. Go to `https://vercel.com/new`.
2. Import the repository.
3. Set the project root to `secure-file-integrity` if this folder is inside a larger repository.
4. Framework Preset can stay as `Other`.
5. Leave Build Command empty.
6. Leave Output Directory empty.
7. Deploy.

## 4. Add Environment Variables

In Vercel:

```text
Project Settings -> Environment Variables
```

Add:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-key
FLASK_SECRET_KEY=your-random-secret
```

Use the same values from local `.env`, but never commit `.env`.

## 5. Redeploy

After adding environment variables:

```text
Project -> Deployments -> Redeploy
```

## 6. Test the Live App

Open the Vercel URL and test:

1. Register Original File.
2. Check File Authenticity with the same file.
3. Modify the file and verify again.
4. Open Dashboard.

## Important Notes

- Vercel runs Flask as a serverless function.
- Uploaded files are saved only temporarily while hashing.
- Supabase stores the important data: filename, hash, status, and timestamp.
- Do not rely on Vercel local storage for permanent file storage.
