# Shakespeare Showcase

**a CHRIS KELLY production** · Teatre Gaudí Barcelona · Thursdays–Saturdays in March 2027 · Curtain 20:00

The production site for a showcase of scenes from seven Shakespeare plays: the running order, the scripts, cast and crew, Saturday rehearsals, rehearsal booking and the marketing materials.

## What's here

| Path | Contents |
|---|---|
| `index.html` | The site: a single file with no build step. |
| `posters/jpg/` | All posters at full size: 8 designs × Instagram 1080×1350 and TikTok/Stories 1080×1920, plus the ticket. |
| `posters/source/` | The poster generator (`gen.py`, which builds SVG/HTML) and the renderer (`shoot.js`, Playwright). |
| `scripts/scenes.json` | Full text of every scene used, taken from the public-domain Moby Shakespeare (via okfn/shakespeare-material). |
| `scripts/extract.py` | The script that extracts those scenes. |

## Key details

- **Shows:** Teatre Gaudí Barcelona, Carrer de Sant Antoni Maria Claret, 120, 08025 Barcelona. Every Thursday, Friday and Saturday in March 2027 (12 performances). Arrive 18:00, warm-up 18:30–19:30, curtain 20:00. Tech on Wed 3 March (approx.).
- **Saturday rehearsals:** Centre Cultural Albareda, Carrer d'Albareda 22–24, 08004 Barcelona. 09:00–11:00, 23 Jan – 27 Feb 2027.
- **Weekday sessions:** Barcelona Code School, Carrer de París 157, 08036 Barcelona. Mon–Fri 15:30–19:30.

## Note on hosting

The live features (bookings, attendance, accepting parts and headshot uploads) use the Claude artifact runtime. When the site is hosted elsewhere, for example on GitHub Pages, the content pages work fully: running order, scripts, cast, characters, shows, marketing and posters. The live features show as read-only.
