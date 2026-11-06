# Selected Works of Shakespeare

**A CHRIS KELLY PRODUCTION** · Barcelona, venue to be announced · Opens Friday 23 April 2027 (Shakespeare's birthday), then Thursdays–Saturdays to 15 May · Curtain 20:00

**Love · Power · Madness · Hate.** The production site for an evening of scenes from eight Shakespeare plays: the running order, the scripts, the company, Saturday rehearsals, rehearsal booking, the marketing materials and the pitch for theatres (`#pitch`).

Live at [shakespeareshow.actor](https://shakespeareshow.actor) (and chrisinbarcelona.github.io/shakespeare-showcase).

## Names

| Where | Name |
|---|---|
| Official title (tickets, venue listing, press, programme) | **Selected Works of Shakespeare** |
| Campaign titles (posters, social) | **The Love / The Power / The Madness / The Hate of Shakespeare** |

Themes by play: Love = Midsummer, Shrew, As You Like It, Romeo and Juliet · Power = Macbeth, Richard III · Madness = Hamlet (and Lady Macbeth) · Hate = Coriolanus (and Richard III).

## What's here

| Path | Contents |
|---|---|
| `index.html` | The site: a single file with no build step. |
| `posters/jpg/` | All posters at full size, Instagram 1080×1350 and TikTok/Stories 1080×1920: the company poster, the four theme posters, the seven play posters, plus the ticket. |
| `posters/thumb/` | Small versions used on the site's Marketing page. |
| `posters/source/` | The poster generator (`gen.py`) and renderer (`shoot.js`, Playwright). Same emblems and colours as before; type and layout match the website (Inter Tight / Inter, left-aligned two-tone titles, colour tags). Run: `python3 gen.py <fonts dir> build && node shoot.js build`. Fonts: Inter and Inter Tight from @fontsource. |
| `supabase/setup.sql` | Database tables, access rules and activity log (the director code is set privately). |
| `scripts/scenes.json` | Text of every scene used, from **The Folger Shakespeare** (Folger Shakespeare Library, ed. Mowat & Werstine, CC BY-NC), our text of record. Each scene carries its Folger line range and a link to the scene on folger.edu. |
| `scripts/extract.py` | Extracts those scenes from the Folger TEI files (as packaged by DraCor: `git clone https://github.com/dracor-org/shakedracor`, then `python3 extract.py shakedracor/tei scenes.json`). Excerpts (Hamlet 3.1, Romeo and Juliet 1.1) and cut speeches are set at the top of the file. |

## Key details

- **Shows:** Venue to be announced (Barcelona). Opening night Friday 23 April 2027, Shakespeare's birthday and Sant Jordi; then every Thursday, Friday and Saturday to Saturday 15 May (11 performances). Arrive 18:00, warm-up 18:30–19:30, curtain 20:00. Tech on Thu 22 April (approx.).
- **Saturday rehearsals:** Centre Cultural Albareda, Carrer d'Albareda 22–24, 08004 Barcelona. 09:00–11:30, every Saturday 7 Nov 2026 – 17 Apr 2027 (breaks 26 Dec, 2 Jan, 27 Mar). Full run-throughs on 3, 10 and 17 April.
- **Weekday sessions:** Barcelona Code School, Carrer de París 157, 08036 Barcelona. Mon–Fri 15:30–19:30.

## Saving

Accepting parts and roles, bookings, attendance and director's notes are saved in Supabase. Everyone picks their name in My panel; editing notes and settings needs the director code.
