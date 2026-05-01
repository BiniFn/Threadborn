create table if not exists reader_reactions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references users(id) on delete cascade,
  novel_id text not null default 'threadborn',
  target_type text not null check (target_type in ('volume', 'chapter')),
  volume_id text not null,
  chapter_id text,
  rating smallint check (rating between 1 and 5),
  category text not null default 'comment' check (category in ('comment', 'theory', 'spoiler')),
  content text not null default '',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists idx_reader_reactions_target on reader_reactions(novel_id, target_type, volume_id, chapter_id, created_at desc);
create index if not exists idx_reader_reactions_user on reader_reactions(user_id, created_at desc);
create index if not exists idx_reader_reactions_rating on reader_reactions(novel_id, target_type, volume_id, chapter_id, rating);
