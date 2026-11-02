-- Shakespeare Showcase: Supabase setup
-- Paste all of this into Supabase → SQL Editor → New query, then click Run.
-- Safe to run more than once.

-- 1. One table holds everything the site saves:
--    cast (who accepted / declined), bookings, attendance, content (director notes, settings).
create table if not exists public.docs (
  collection text not null,
  id         text not null,
  data       jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now(),
  primary key (collection, id)
);
alter table public.docs enable row level security;

-- Anyone with the site can read.
drop policy if exists "read all" on public.docs;
create policy "read all" on public.docs for select to anon, authenticated using (collection <> 'outreach');  -- the Venues tracker is director-only (see venues-private.sql)

-- Anyone with the site can accept/decline, mark attendance and book a scene slot.
-- Director-only things (notes, settings, blocked-out slots, company calls) go through director_write below.
drop policy if exists "company insert" on public.docs;
create policy "company insert" on public.docs for insert to anon, authenticated
  with check (collection in ('cast','attendance') or (collection = 'bookings' and data->>'type' = 'scene'));
drop policy if exists "company update" on public.docs;
create policy "company update" on public.docs for update to anon, authenticated
  using      (collection in ('cast','attendance') or (collection = 'bookings' and data->>'type' = 'scene'))
  with check (collection in ('cast','attendance') or (collection = 'bookings' and data->>'type' = 'scene'));
drop policy if exists "company delete" on public.docs;
create policy "company delete" on public.docs for delete to anon, authenticated
  using (collection = 'attendance' or (collection = 'bookings' and data->>'type' = 'scene'));

grant select, insert, update, delete on public.docs to anon, authenticated;

-- 2. Activity log: every change is recorded, so you can see (and undo) anything odd.
--    Only visible to you in the Supabase dashboard (Table Editor → activity).
create table if not exists public.activity (
  id         bigserial primary key,
  at         timestamptz not null default now(),
  op         text,
  collection text,
  doc_id     text,
  old_data   jsonb,
  new_data   jsonb
);
alter table public.activity enable row level security;  -- no policies = not readable from the site

create or replace function public.log_docs() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  insert into activity (op, collection, doc_id, old_data, new_data)
  values (tg_op,
          coalesce(new.collection, old.collection),
          coalesce(new.id, old.id),
          case when tg_op <> 'INSERT' then old.data end,
          case when tg_op <> 'DELETE' then new.data end);
  return coalesce(new, old);
end $$;
drop trigger if exists docs_log on public.docs;
create trigger docs_log after insert or update or delete on public.docs
  for each row execute function public.log_docs();

-- 3. Director code: unlocks editing notes, settings and blocking slots on the site.
create table if not exists public.director (pin text not null);
alter table public.director enable row level security;  -- not readable from the site
delete from public.director;
insert into public.director (pin) values ('CHANGE-ME-TO-A-SECRET-CODE');

create or replace function public.is_director(p_pin text) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from director where pin = p_pin)
$$;

create or replace function public.director_write(p_pin text, p_collection text, p_id text,
                                                 p_data jsonb default '{}'::jsonb, p_delete boolean default false)
returns void language plpgsql security definer set search_path = public as $$
begin
  if not exists (select 1 from director where pin = p_pin) then
    raise exception 'not allowed' using errcode = '42501';
  end if;
  if p_delete then
    delete from docs where collection = p_collection and id = p_id;
  else
    insert into docs (collection, id, data, updated_at) values (p_collection, p_id, p_data, now())
    on conflict (collection, id) do update set data = excluded.data, updated_at = now();
  end if;
end $$;

grant execute on function public.is_director(text) to anon, authenticated;
grant execute on function public.director_write(text, text, text, jsonb, boolean) to anon, authenticated;

-- 4. Venues tracker: readable only with the director code.
create or replace function public.director_read(p_pin text, p_collection text)
returns table(id text, data jsonb)
language plpgsql stable security definer set search_path = public as $$
begin
  if not exists (select 1 from director where pin = p_pin) then
    raise exception 'not allowed' using errcode = '42501';
  end if;
  return query select d.id, d.data from docs d where d.collection = p_collection;
end $$;
grant execute on function public.director_read(text, text) to anon, authenticated;
