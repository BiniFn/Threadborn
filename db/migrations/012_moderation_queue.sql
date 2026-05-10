create table if not exists moderation_requests (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references users(id) on delete cascade,
  request_type text not null check (
    request_type in (
      'profile_update',
      'avatar_update',
      'reader_reaction',
      'community_post',
      'community_comment'
    )
  ),
  status text not null default 'pending' check (status in ('pending', 'approved', 'rejected')),
  payload jsonb not null default '{}'::jsonb,
  target_table text,
  target_id uuid,
  reviewed_by uuid references users(id) on delete set null,
  review_note text,
  reviewed_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists idx_moderation_requests_status_created
  on moderation_requests(status, created_at desc);

create index if not exists idx_moderation_requests_user_created
  on moderation_requests(user_id, created_at desc);
