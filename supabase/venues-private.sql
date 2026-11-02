-- Make the Venues tracker (collection 'outreach') readable only with the director code.
-- Paste into Supabase → SQL Editor → New query → Run. Safe to run more than once.
-- Run THIS file on its own: re-running setup.sql would reset your director code.

-- Everyone can still read everything else; 'outreach' is no longer readable from the site.
drop policy if exists "read all" on public.docs;
create policy "read all" on public.docs for select to anon, authenticated
  using (collection <> 'outreach');

-- The site reads the tracker through this function, which checks the director code.
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
