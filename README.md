# Selected Works of Shakespeare

**A CHRIS KELLY PRODUCTION** · Teatre Gaudí Barcelona · Thursdays–Saturdays in March 2027 · Curtain 20:00

**Love · Power · Madness · Hate.** The production site for an evening of scenes from seven Shakespeare plays: the running order, the scripts, the company, Saturday rehearsals, rehearsal booking and the marketing materials.

Live at [shakespeareshow.actor](https://shakespeareshow.actor) (and chrisinbarcelona.github.io/shakespeare-showcase).

## Names

| Where | Name |
|---|---|
| Official title (tickets, venue listing, press, programme) | **Selected Works of Shakespeare** |
| Campaign titles (posters, social) | **The Love / The Power / The Madness / The Hate of Shakespeare** |

Themes by play: Love = Midsummer, Shrew, As You Like It · Power = Macbeth, Richard III · Madness = Hamlet (and Lady Macbeth) · Hate = Coriolanus (and Richard III).

## What's here

| Path | Contents |
|---|---|
| `index.html` | The site: a single file with no build step. |
| `posters/jpg/` | All posters at full size, Instagram 1080×1350 and TikTok/Stories 1080×1920: the company poster, the four theme posters, the seven play posters, plus the ticket. |
| `posters/thumb/` | Small versions used on the site's Marketing page. |
| `posters/source/` | The poster generator (`gen.py`) and renderer (`shoot.js`, Playwright). Same emblems and colours as before; type and layout match the website (Inter Tight / Inter, left-aligned two-tone titles, colour tags). Run: `python3 gen.py <fonts dir> build && node shoot.js build`. Fonts: Inter and Inter Tight from @fontsource. |
| `supabase/setup.sql` | Database tables, access rules and activity log (the director code is set privately). |
| `scripts/scenes.json` | Full text of every scene used, taken from the public-domain Moby Shakespeare (via okfn/shakespeare-material). |
| `scripts/extract.py` | The script that extracts those scenes. |

## Key details

- **Shows:** Teatre Gaudí Barcelona, Carrer de Sant Antoni Maria Claret, 120, 08025 Barcelona. Every Thursday, Friday and Saturday in March 2027 (12 performances). Arrive 18:00, warm-up 18:30–19:30, curtain 20:00. Tech on Wed 3 March (approx.).
- **Saturday rehearsals:** Centre Cultural Albareda, Carrer d'Albareda 22–24, 08004 Barcelona. 09:00–11:00, 23 Jan – 27 Feb 2027.
- **Weekday sessions:** Barcelona Code School, Carrer de París 157, 08036 Barcelona. Mon–Fri 15:30–19:30.

## Saving

Accepting parts and roles, bookings, attendance and director's notes are saved in Supabase. Everyone picks their name in My panel; editing notes and settings needs the director code.
