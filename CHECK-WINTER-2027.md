# Independent check: Winter 2027 change

**Checked:** origin/main `1d3d33b` (diff from old main `eb8cc87`), checked on 22/11/2026.
**Verdict: PASS WITH NOTES.** Every figure is correct. The page works at 360 px. Every brief item is met. Two problems in the add-a-round tool should be fixed before 29/11 (F1, F2).

## What I ran
- `git diff eb8cc87 origin/main` (15 files: 13 changed, 0 deleted). I read all of the new code.
- I rendered the live round-2 page from http://127.0.0.1:8765 with headless Chrome (`--dump-dom`) and pulled out the text.
- I made my own test copies of the **current** page, because the :8766 copy is an older build. One has 7 rounds and one has 3 rounds with a tie at the top. I rendered each twice and compared the output byte for byte.
- `tools/winter_add_round.py --dry-run` with 10 inputs. The data file's md5 was the same before and after.
- A 360 px iframe probe measured scrollWidth and any element running past the right edge on 4 pages.
- I looked at 4 screenshots and grepped every page's nav. I checked that `changes.js` and `.github` have no diff.

## Totals: my sums against the page (after round 2)
| Player | Expected total | Shown | Expected pos | Shown |
|---|---|---|---|---|
| Sid Amin | 34+27 = 61 | 61 | 1 | 1 |
| Imran K (incl. "Imran K T") | 33+27 = 60 | 60 | T2 | T2 |
| Tariq Javaid | 37+23 = 60 | 60 | T2 | T2 |
| Raz Shafi | 32+20 = 52 | 52 | 4 | 4 |
| Shufqat Khan | 22+18 = 40 | 40 | 5 | 5 |
| Guftar Hussain | 31 | 31 | 6 | 6 |
| Yaseen Mohammed | 30 | 30 | 7 | 7 |
| Mansoor M | 29 | 29 | 8 | 8 |
| Waseem Goldenboy | 27 | 27 | 9 | 9 |
| Mahmood Sadiq | 25 | 25 | 10 | 10 |
| Shazad Hussain | 22 | 22 | 11 | 11 |
| Basharat Ali (from "Basharat2 Ali") | 21 | 21 | 12 | 12 |

These all match the page:
- **KPIs:** leader 61 (Sid Amin), gap 1 (to Imran K and Tariq Javaid), best single round 37 (Tariq, 15/11/2026), 12 players and 17 cards in 2 rounds.
- **Takeaways:** 5 Sundays to go, 12 of 12 players can still reach 6 counting scores.
- **Round winners:** R1 Tariq Javaid 37, field of 6, average 30.5 (183/6). R2 Guftar Hussain 31, field of 11, average 25.0 (275/11).

**Crystal ball form values, worked out by hand.** Field average is 458/17 = 26.94. The 2025 mean is 2908/11/8 = 33.05.

| Player | Working | Form | Page |
|---|---|---|---|
| Sid Amin | prior 25.90, (61 + 2×25.90)/4 | 28.2 | 28.2 |
| Imran K | (60 + 2×26.27)/4 | 28.1 | 28.1 |
| Tariq Javaid | prior = field average, (60 + 2×26.94)/4 | 28.5 | 28.5 |
| Guftar Hussain | (31 + 2×26.77)/3 | 28.2 | 28.2 |
| Mahmood Sadiq | (25 + 2×24.15)/3 | 24.4 | 24.4 |

The crystal ball's maths is sound and honest:
- It gives the same result every time for the same data. There is no Math.random, and two renders were identical.
- It uses the best-6 rule in every run-through.
- When players tie at the top of a run-through, the win is shared between them.
- It does not crash with 2, 3 or 7 rounds.
- It is labelled "Just for fun between friends. Not a result, and no bets."

**Stress tests on my copy of the current page:**
- **7 rounds:** Imran K's 26 (R5) and Sid Amin's 27 (R2) are greyed and struck through. Totals are 216−26 = 190 and 216−27 = 189, which are correct. The page says "Final report" and the season hub shows "Final".
- **Tie after 3 rounds:** "Imran K and Sid Amin share the lead on 95". Both show T1, and the next player shows 3. The gap KPI is 0, "Level at the top". It says 5 of 12 can still reach 6, which is correct.

**Add-a-round tool:**
- Good input: the aliases map correctly.
- Refused, as they should be: a misspelt name, a duplicate date, points of 74, a non-Sunday date, the same player twice through an alias, 3-digit points, a name in lower case.

**Other checks:**
- **Nav:** the 2027 season link is on all 10 existing pages plus the 2 new ones. `changes.html` never had a nav, so it is unchanged and correct.
- **Untouched:** `changes.js` and `.github` have no diff, and no files were deleted.
- **Print CSS:** opacity and animation are switched off, print-color-adjust is set to exact, the nav is hidden, and each exhibit starts on a new page.
- **Phone layout:** at a 360 px viewport the scrollWidth is 345 on winter-2027, season-2027, index and season. No element runs past the edge apart from the matrix, which scrolls inside its own box.

## Findings
| # | Sev | Where | Finding | Proposed fix |
|---|---|---|---|---|
| F1 | Medium | tools/winter_add_round.py:62-66; winter-2027.html:238, 304, 387-390 | The tool accepts any winter date, even out of order: it took 13/12/2026 with 29/11 missing. It always adds the round at the end. The page places rounds by their position in the file, not by date. So if a Sunday is skipped or entered late, its scores show under the wrong date, and the "N of 7 played" count is wrong. | On the page, place each round with `W.dates.indexOf(r.date)` and count played as the highest index + 1. In the tool, insert the round in date order, or refuse any date earlier than one already entered. |
| F2 | Medium | tools/winter_add_round.py:64-65 | A name with an apostrophe (with `--new "Tom O'Neil"`) is written as `['Tom O'Neil', ...]`. That breaks the JavaScript, and the whole page goes blank. | Write names with `json.dumps(name)`, or refuse names containing `'`. |
| F3 | Low | winter-2027.html:290 | The gap KPI reads "1 points to …". | Use "point" when the gap is 1. |
| F4 | Low | winter-2027.html:364-376 | In the final report, Exhibit 2 still lists form rows and says "The 0 remaining Sundays are then played 5,000 times". | When the tournament is over, show the champion line only and hide the rows and the "How it guesses" text. |
| F5 | Low (info) | winter-2027.html:318-319, 335 | Tariq Javaid played 5 rounds in 2025 (SF_UNRANKED), but he is treated as "no 2025 record" and set level with the field. It also assumes every player turns up every Sunday (line 337), which helps players who have missed rounds (e.g. Mansoor at 9% from one card). Both are disclosed in the "How it guesses" text, so this is fine. | Optional: reword to "no ranked 2025 record". |
| F6 | Low | winter-2027.html:249-252 | `proj` and `reach6` are left over from the old projection and are never used. | Delete them. |
| F7 | Low | season-2027.html (inline script) | The best-6 rule is written a second time in the hub page, so the two could drift apart. | Share one helper, or have the hub read a total the report exposes. |
| F8 | Low (evidence) | docs-winter-2027/*-360.png | The 360 px screenshots are cut off on the right on every page, including the existing index. They look like a wider render that was cropped, not real overflow (the probe shows none). | Retake them with device emulation, e.g. Chrome DevTools at 360×800, so the proof matches what a phone shows. |
| F9 | Info | :8766 test copy | That scratch copy uses the older "banked versus projected" Exhibit 2, not the crystal ball. | Rebuild it from origin/main if it is used again. |
| F10 | Cosmetic | winter-2027.html:93 | At 1280 px, the crystal ball sub-line wraps as "now T2 on / 60". | Widen the name column, e.g. `minmax(92px,220px)`. |

**Verdict: PASS WITH NOTES**

## Fixes applied after this check (builder, branch claude/winter-2027-check)
- F1 fixed: the page places each round by its date (`W.dates`), not its position in the file; a skipped
  Sunday shows "no round", future ones "to play". The tool inserts rounds in date order. Tested on a scratch
  copy with 13/12 entered before 29/11 and 06/12 skipped: columns, winners table and "4 of 7 played" correct.
- F2 fixed: the tool refuses names containing quote marks, `<`, `>` or `\` (tested with "Tom O'Neil").
- F3 fixed: "1 point to ...". F4 fixed: final report shows only the champion line in Exhibit 2.
- F5 reworded ("if they were ranked in the 2025 Stableford Series; unranked players start level").
- F6 removed unused `proj`/`reach6`. F10 name column widened to 220px.
- Not changed: F7 (season page repeats the best-6 sum; small, noted), F8 (360 px screenshots are cropped by
  headless Chrome's minimum window width; a 360 px browser check showed scrollWidth 360 = no overflow), F9 (scratch copy only).
- Live figures re-checked after the fixes: same 12 rows, Sid Amin 61 first, crystal ball unchanged, 0 console errors.
