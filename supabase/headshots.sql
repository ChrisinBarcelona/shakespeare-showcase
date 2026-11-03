-- Shakespeare Showcase: let actors upload their own headshot from My panel.
-- Paste into Supabase → SQL Editor → New query, then click Run. Safe to run more than once.
-- Photos are resized in the browser (max 800px JPEG) and saved in the "headshots" collection.
-- Only images are accepted, capped at about 1.5 MB. Deleting stays director-only.

drop policy if exists "headshot insert" on public.docs;
create policy "headshot insert" on public.docs for insert to anon, authenticated
  with check (collection = 'headshots'
              and data->>'img' like 'data:image/%'
              and length(data->>'img') < 1500000);

drop policy if exists "headshot update" on public.docs;
create policy "headshot update" on public.docs for update to anon, authenticated
  using      (collection = 'headshots')
  with check (collection = 'headshots'
              and data->>'img' like 'data:image/%'
              and length(data->>'img') < 1500000);
