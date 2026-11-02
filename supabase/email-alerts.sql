-- Email alerts: emails Chris whenever someone accepts or declines a part or crew role.
-- Sends through Resend (resend.com, free tier). Paste into Supabase → SQL Editor → Run.
-- Safe to run more than once. Does nothing until the Resend key is saved (step at the bottom).

create extension if not exists pg_net with schema extensions;

create table if not exists public.alert_settings (
  id int primary key default 1 check (id = 1),
  to_email text not null default 'chris@chriskelly.it',
  from_email text not null default 'Shakespeare Show <onboarding@resend.dev>'
);
alter table public.alert_settings enable row level security;  -- not readable from the site
insert into public.alert_settings (id) values (1) on conflict (id) do nothing;

create or replace function public.alert_cast_change() returns trigger
language plpgsql security definer set search_path = public, extensions as $$
declare
  k text; s alert_settings; who text; f text; st text; was text; what text; verb text; html text;
begin
  if new.collection <> 'cast' then return new; end if;
  select decrypted_secret into k from vault.decrypted_secrets where name = 'resend_api_key' limit 1;
  if k is null then return new; end if;
  select * into s from alert_settings where id = 1;
  who := coalesce(nullif(new.data->>'name', ''), initcap(replace(new.id, '-', ' ')));

  -- 'status' = acting part(s); 'crewStatus' = crew role for someone who also acts
  foreach f in array array['status', 'crewStatus'] loop
    st  := coalesce(new.data->>f, '');
    was := case when tg_op = 'UPDATE' then coalesce(old.data->>f, '') else '' end;
    continue when st = was or st not in ('accepted', 'pending', 'declined');
    continue when st = 'pending' and was = '';  -- not an answer, just a new record
    what := case f when 'crewStatus' then 'crew role' else 'part' end;
    verb := case st when 'accepted' then 'accepted their ' || what
                    else 'declined their ' || what || ' (set back to pending)' end;
    html := format(
      '<p style="font:16px Arial,sans-serif"><b>%s</b> %s on the show site.</p>'
      '<p style="font:14px Arial,sans-serif;color:#555">%s</p>'
      '<p style="font:14px Arial,sans-serif"><a href="https://shakespeareshow.actor/?full#cast">See the company</a></p>',
      who, verb, to_char(now() at time zone 'Europe/Madrid', 'Dy DD Mon, HH24:MI'));
    perform net.http_post(
      url := 'https://api.resend.com/emails',
      headers := jsonb_build_object('Authorization', 'Bearer ' || k, 'Content-Type', 'application/json'),
      body := jsonb_build_object(
        'from', s.from_email, 'to', jsonb_build_array(s.to_email),
        'subject', who || case st when 'accepted' then ' accepted ✓' else ' declined' end
                   || ' · Selected Works of Shakespeare',
        'html', html));
  end loop;
  return new;
exception when others then
  return new;  -- an email problem must never block someone accepting their part
end $$;

drop trigger if exists cast_email_alert on public.docs;
create trigger cast_email_alert after insert or update on public.docs
  for each row execute function public.alert_cast_change();

-- LAST STEP (Chris does this himself, with his own key from resend.com → API Keys):
--   select vault.create_secret('re_PASTE_YOUR_KEY_HERE', 'resend_api_key');
-- To replace the key later:
--   select vault.update_secret((select id from vault.secrets where name = 'resend_api_key'), 're_NEW_KEY');
