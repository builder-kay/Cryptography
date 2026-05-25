create extension if not exists "pgcrypto";

create table if not exists public.files (
    id uuid primary key default gen_random_uuid(),
    filename text not null,
    sha256_hash text not null,
    verification_status text not null,
    upload_timestamp timestamp default now()
);

create unique index if not exists files_filename_unique
on public.files (filename);

alter table public.files enable row level security;

create policy "Allow file integrity demo select"
on public.files
for select
using (true);

create policy "Allow file integrity demo insert"
on public.files
for insert
with check (true);

create policy "Allow file integrity demo update"
on public.files
for update
using (true)
with check (true);
