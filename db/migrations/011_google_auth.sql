alter table users
  add column if not exists google_id text;

create unique index if not exists idx_users_google_id_unique
  on users(google_id)
  where google_id is not null;
