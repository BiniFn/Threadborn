alter table users
  add column if not exists community_banned_until timestamptz,
  add column if not exists community_ban_reason text;

create index if not exists idx_users_community_banned_until
  on users(community_banned_until);
