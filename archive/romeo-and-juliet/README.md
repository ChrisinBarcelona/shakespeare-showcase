# Romeo and Juliet: archived

Archived 21 Nov 2026. Romeo and Juliet is off the first version of the show (BCN Studio). It comes back for the Teatre Gaudí run in 2028. The site doesn't load anything in this folder.

The whole site as it was with R&J is saved on the branch **`full-show-with-rj`** (commit `453f5dc`).

## What's in here

| File | What it holds |
|---|---|
| `scenes.json` | All six R&J scenes, with Chris's cuts marked (Folger text, same format as `scripts/scenes.json`) |
| `site-data.json` | Everything removed from `index.html`, word for word: characters and bios, parts and word counts, running-order cards with synopses and ideas, transitions, script notes, "About this scene" panels, speaker map, the 1.1 backdrop, and the original wording of every line that was rewritten |

`scripts/extract.py` still has all the R&J cuts. Running it rewrites this folder's `scenes.json` and leaves the live show alone.

Related project docs in the claude.ai Project (Shakespeare Showcase): `balcony-cut.md` and `juliet-song-brief.md` (Juliet's song, "Give Me My Romeo").

## The scenes and where they sat

| Scene | Title | Came after | Went before |
|---|---|---|---|
| 1.3 | Thinks she of marriage? (Juliet, Lady Capulet, Nurse) | Macbeth 1.3 | As You Like It 2.1 |
| 1.1 | Good morrow, cousin (Romeo, Benvolio) | Coriolanus 4.5 | R&J 1.4 |
| 1.4 | Queen Mab (Mercutio, Romeo, Benvolio) | R&J 1.1 | R&J 1.5 |
| 1.5 | The Capulet feast (Capulet, Romeo, Juliet, Tybalt, Nurse, Benvolio, Servingman) | R&J 1.4 | Hamlet 3.1 |
| 2.2 | Wherefore art thou Romeo? (Juliet's two speeches only) | Ophelia's silhouette | Midsummer 3.2 |
| 5.3 | Thus with a kiss I die (Romeo, Juliet, Friar Lawrence) | Midsummer 4.1 | End of show |

Casting at the time: Sarah Burns as Juliet. Every other R&J part was vacant.

## What was linked to it (restage these when it comes back)

- **The nunnery scene was played inside the Capulet feast.** Hamlet and Ophelia were two more guests at the party, and the crowning mosaic picked up as the party drained away.
- **Juliet's song** came in out of Ophelia's silhouette into the balcony, and returned softly after the tomb into the curtain call.
- **The tomb (5.3) closed the show.** Midsummer 4.1 handed over with a tolling bell, and Juliet was already laid out on the bier.
- **Transitions rewritten for the BCN Studio version:** Macbeth 1.3 → Arden, Coriolanus 4.5 → nunnery, silhouette → Midsummer 3.2, and Midsummer 4.1 now ends the show. The originals are in `site-data.json`.
- **Counts that changed:** eight plays became seven, the make-up vacancy now says 7 plays, Love lost R&J on the themes, and two rehearsal-schedule lines dropped it (16 Jan blocking, 27 Feb scene work).
- **Left in the site on purpose:** the R&J colours (`ACC_LIGHT`, `PLAYCOL`, `PLAYACC`) and the `scriptPlay` name lookup. They're harmless and save work when R&J comes back.

## Bringing it back

Put the `site-data.json` entries back into the same constants in `index.html` at the positions above, add the six scenes back to `SCRIPTS` and `scripts/scenes.json`, remove `ARCHIVED` from `scripts/extract.py`, then renumber the scenes and restore the rewritten lines. Or compare against the `full-show-with-rj` branch.
