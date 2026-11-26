-- Make the Emails page (collection 'contacts') readable only with the director code.
-- Paste into Supabase → SQL Editor → New query → Run. Safe to run more than once.
-- Writing to it already needs the director code (director_write).
drop policy if exists "read all" on public.docs;
create policy "read all" on public.docs for select to anon, authenticated
  using (collection not in ('outreach', 'applications', 'todos', 'contacts'));
