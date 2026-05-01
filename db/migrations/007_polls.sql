create table if not exists polls (
  id uuid primary key default gen_random_uuid(),
  question text not null,
  lang varchar(10) default 'en',
  is_active boolean default true,
  created_at timestamptz default now()
);

create table if not exists poll_options (
  id uuid primary key default gen_random_uuid(),
  poll_id uuid references polls(id) on delete cascade,
  option_text text not null,
  votes integer default 0
);
