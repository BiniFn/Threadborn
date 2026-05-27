alter table posts
  drop constraint if exists posts_category_check;

alter table posts
  add constraint posts_category_check
  check (category in ('chat', 'fan_art', 'theory', 'spoiler'));
