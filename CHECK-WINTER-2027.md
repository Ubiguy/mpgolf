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

## Re-check: January extension (e3af8b7)
Independent checker, 22/11/2026. Reviewed `git diff origin/main..HEAD` (1d3d33b..e3af8b7) in full:
data-winter-2027.js, winter-2027.html, season-2027.html, tools/winter_add_round.py, PLAN.md, CHECK file, screenshots.
Nothing in the repo was changed except this file. Stress tests ran on a copy in the session scratchpad
(served on 127.0.0.1:8777); the real data file was never written.

**What was run**
- Weekday of all 12 dates with Python `datetime`: every one is a Sunday (15/11/2026 … 27/12/2026, 03/01, 10/01, 17/01, 24/01, 31/01/2027).
- `sha256sum data-winter-2027.js` = `15624e1d…`; both pages load `data-winter-2027.js?v=15624e1d`. `tools/release.py verify`: consistent.
- grep for "seven", "Seven", "27/12", "repeat(7" in the four diff'd files: only the 27/12 date itself in the list and the word table `WORDS`. No stale text on the pages.
- Headless Chrome `--dump-dom` of winter-2027.html and season-2027.html from 127.0.0.1:8765; all figures re-added by hand. 0 console errors on both. Two renders are byte-identical (crystal ball is deterministic).
- 360 px: page loaded in a 360 px iframe and measured, plus a screenshot. winter-2027: scrollWidth = clientWidth (345, no sideways page scroll); matrix scrolls inside `.mx-wrap` (303 of 752 px, overflow-x auto); winners table 306/305 (1 px, nothing visible); no element outside a scroll box passes the edge; progress dots 22.7 px each. season-2027: 360/360.
- Tool, `--dry-run` on the copy: 07/02/2027 refused (not in list); 28/11/2026 (a Saturday) refused; "Tom O'Neil" with `--new` refused; `Tom "Big" Smith` refused; 31/01/2027 accepted; duplicate 10/01/2027 refused.
- Stress, on the copy: added 10/01/2027 first, then 29/11, 06/12, 20/12, 27/12, 03/01, 17/01 (13/12 skipped). File came out in date order. Then 24/01 and 31/01, still skipping 13/12. Then 13/12 late, to reach a full 12.

**Expected vs shown (live data)**
| Item | Expected (by hand) | Shown |
|---|---|---|
| Lead / cover | 12 Sundays, 15/11/2026 to 31/01/2027 | "Twelve Sundays at Leeds Golf Centre, Wike Ridge, 15/11/2026 to 31/01/2027" |
| Progress strip | 12 dots, 2 on; 15/11 … 31/01 | 12 dots, 2 on; "15/11 · 2 of 12 played · 31/01" |
| Totals | Sid 34+27=61; Imran 33+27=60; Tariq 37+23=60; Raz 52; Shufqat 40; Guftar 31; Yaseen 30; Mansoor 29; Waseem 27; Mahmood 25; Shazad 22; Basharat 21 | same, positions 1, T2, T2, 4 … 12 |
| KPIs | 61 Sid; gap 1; best round 37 Tariq 15/11/2026; 12 players, 17 cards in 2 rounds | same ("1 point to Imran K and Tariq Javaid") |
| Takeaways | 10 Sundays to go; 12 of 12 can reach 6; decided 31/01/2027 | same |
| Winners table | R1 Tariq 37, 6, 30.5 (183/6); R2 Guftar 31, 11, 25.0 (275/11); R3–R12 "to play" | same |
| Round chart | R1, R2 rows + one "R3-R12 · 10 to play, 29/11 to 31/01" row | same |
| Crystal ball | 10 Sundays left; field average 458/17 = 26.9; deterministic | "The 10 remaining Sundays"; 26.9; Tariq 33%, Sid 17%, Imran 14%, Mansoor 11% (dark horse), Guftar 10%, Yaseen 10%, Raz 2%, Waseem 2%, others <1% (sums to ~100) |
| Method | best 6 count, more than 6 → rest drop; decided 31/01/2027; 12 dates listed | same |
| Season hub | "12 Sundays … 15/11/2026 to 31/01/2027 … 2 of 12 played: Sid Amin leads on 61"; chip Live | same |

**Expected vs shown (stress copy)**
| Case | Expected | Shown |
|---|---|---|
| 9 rounds, 13/12 skipped | Sid 34,27,20,25,31,19,33,40,29 → best 6 = 194, greys 20, 25, 19; Imran → 190, greys 27, 28, 26 | same; 13/12 column "no round"; 24/01, 31/01 "to play"; winners table and chart rows by date |
| 11 rounds, 13/12 never played, 31/01 in | Imran 205, Sid 194; season over | figures right, but "1 Sunday to go", crystal ball 99%, not "Final"; hub chip "Live" (see R1) |
| All 12 (13/12 added last) | Sid 45,40,34,33,31,29 = 212 (6 greys); Imran 38,36,35,33,32,31 = 205 (6 greys) | same; "Final report"; crystal ball shows champion line only; hub chip "Final" |

**Findings**
| # | Sev | Where | Finding | Proposed fix |
|---|---|---|---|---|
| R1 | Medium | winter-2027.html:231, 263, 265, 289, 380; season-2027.html:80 | A Sunday with no round (e.g. cancelled for frost) still counts as "to go". With 13/12 skipped and 31/01 entered, the page says "1 Sunday to go", runs the crystal ball for one more Sunday, never shows "Final report", and the hub chip stays "Live". After 9 rounds with a gap it said "after round 9" when the latest is R10, and "3 Sundays to go" when 2 remain. Figures (totals, greys, positions) stay right. | Count Sundays left as those after the last round played: `left = TOTAL - 1 - lastSlot`; kicker "after round ${lastSlot+1}"; hub `final` from the same rule. Or document in the tool and data file: "if a Sunday is cancelled, delete its date from `dates`". |
| R2 | Low | winter-2027.html:288 | Final takeaway says "each player's lowest round beyond 6 has been dropped" (from the 7-round era); with 12 rounds up to 6 drop. | "rounds outside each player's best 6 have been dropped". |
| R3 | Low | winter-2027.html:390 | At 360 px the chart's 12-unit text renders at about 8 px (viewBox 420 shown 287 px wide). Readable but small. | Font size 14 in the SVG, or viewBox ~360. |
| R4 | Low | winter-2027.html:315 | A skipped Sunday's cell shows the "still to play" hatch (title "no round" only on hover). | Add a separate light style for "no round", or reword the legend "still to play / no round". |
| R5 | Low | PLAN.md:62 | "No round dropped yet (2 of 7 played)". | "(2 of 12 played)". |
| R6 | Info | season-2027.html:78 | At the end the hub says "Sid Amin leads on 212" next to the "Final" chip (wording existed before this change). | "is champion on" when n === T. |

Earlier fixes confirmed present: rounds placed by date (slot), tool inserts in date order, names with quotes refused.

**Verdict: PASS WITH NOTES**

### Fixes applied after the January re-check (builder)
- R1 fixed: Sundays still to come are now the dates after the latest round entered, so a cancelled Sunday is
  not counted as "to go"; the kicker says "after round <latest>"; the page and the 2027 season hub switch to
  Final once the last Sunday has a round. Tested on a copy with 31/01/2027 entered and other dates skipped:
  "Final report", champion Sid Amin 119 (34+27+28+30), hub "is champion on 119" with the Final chip.
- R2 fixed (wording), R5 fixed (PLAN.md "2 of 12"), R6 fixed (hub says "is champion" when final).
- Not changed: R3 (chart text ~8 px at 360 px, readable), R4 (skipped Sunday uses the "to play" hatch; its
  tooltip and the winners table say "no round").
- Real page re-rendered after the fixes: "after round 2", "2 of 12 played", "10 Sundays to go", totals unchanged.
