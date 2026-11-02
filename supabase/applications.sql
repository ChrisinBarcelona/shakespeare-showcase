-- Vacancy applications: anyone can send the form; only the director can read them;
-- each one emails Chris straight away (uses the Resend key saved for email alerts).
-- Paste into Supabase → SQL Editor → Run. Safe to run more than once.

-- 1. Private reads: the Venues tracker and applications are not readable from the site.
drop policy if exists "read all" on public.docs;
create policy "read all" on public.docs for select to anon, authenticated
  using (collection not in ('outreach', 'applications'));

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

-- 2. Anyone with the site can send an application (insert only, size-limited).
drop policy if exists "company insert" on public.docs;
create policy "company insert" on public.docs for insert to anon, authenticated
  with check (collection in ('cast','attendance')
              or (collection = 'bookings' and data->>'type' = 'scene')
              or (collection = 'applications' and length(data::text) < 4000));

-- 3. Email Chris for every new application.
create or replace function public.esc_html(t text) returns text language sql immutable as $$
  select replace(replace(replace(replace(coalesce(t, ''), '&', '&amp;'), '<', '&lt;'), '>', '&gt;'), '"', '&quot;')
$$;
create or replace function public.alert_application() returns trigger
language plpgsql security definer set search_path = public, extensions as $$
declare k text; s alert_settings; d jsonb := new.data; dt text; html text; is_actor boolean;
begin
  if new.collection <> 'applications' then return new; end if;
  select decrypted_secret into k from vault.decrypted_secrets where name = 'resend_api_key' limit 1;
  if k is null then return new; end if;
  select * into s from alert_settings where id = 1;
  is_actor := (d->>'kind') = 'actor';
  dt := coalesce(to_char((d->>'date')::date, 'Dy DD Mon YYYY'), d->>'date', '') || ' at ' || coalesce(d->>'time', '');
  html := format(
    '<p style="font:16px Arial,sans-serif"><b>%s</b> would love to %s <b>%s</b>.</p>'
    '<p style="font:15px Arial,sans-serif">Proposed: <b>%s</b> at Barcelona Code School</p>'
    '<p style="font:14px Arial,sans-serif">Email: <a href="mailto:%s">%s</a>%s</p>'
    '<p style="font:14px Arial,sans-serif;white-space:pre-wrap;color:#333">%s</p>'
    '<p style="font:13px Arial,sans-serif;color:#777">Reply to this email to answer them directly. All applications are in My panel on shakespeareshow.actor.</p>',
    esc_html(d->>'name'), case when is_actor then 'audition for' else 'meet to discuss the job of' end, esc_html(d->>'role'), esc_html(dt),
    esc_html(d->>'email'), esc_html(d->>'email'), case when coalesce(d->>'phone','') <> '' then ' · Phone: ' || esc_html(d->>'phone') else '' end,
    esc_html(d->>'msg'));
  perform net.http_post(
    url := 'https://api.resend.com/emails',
    headers := jsonb_build_object('Authorization', 'Bearer ' || k, 'Content-Type', 'application/json'),
    body := jsonb_build_object(
      'from', s.from_email, 'to', jsonb_build_array(s.to_email),
      'reply_to', d->>'email',
      'subject', (case when is_actor then 'Audition request: ' else 'Job request: ' end) || (d->>'role') || ' · ' || (d->>'name'),
      'html', html));
  return new;
exception when others then
  return new;  -- never block someone's application because of an email problem
end $$;

drop trigger if exists application_email_alert on public.docs;
create trigger application_email_alert after insert on public.docs
  for each row execute function public.alert_application();
