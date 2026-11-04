-- Shakespeare Showcase: actors can give up (release) one of their parts from My panel.
-- Applied to the live project on 4 Nov 2026. Safe to run more than once.
-- One row per released part in the "releases" collection, id = the part id.
-- Insert only: actors can't edit or delete a release. The director restores a part
-- by deleting the row through director_write (the Restore button in My panel).
drop policy if exists "release insert" on public.docs;
create policy "release insert" on public.docs for insert to anon, authenticated
  with check (
    collection = 'releases'
    and id = data->>'part'
    and id in ('macbeth','aufidius','banquo','hamlet','lady-macbeth','witch-1','kate','hermia','ophelia',
               'witch-2','laertes','gertrude','claudius','coriolanus','witch-3','seyton','helena','anne',
               'polonius','horatio','demetrius','lysander','petruchio','richard','gravedigger',
               'other-gravemaker','puck','oberon','titania','oberons-fairy','amiens','fairy','duke-senior')
    and length(coalesce(data->>'actor','')) between 2 and 80
    and length(data::text) < 2000
  );
