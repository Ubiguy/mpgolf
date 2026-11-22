# PLAN: MPG Winter Tournament 2027 (branch `claude/winter-2027`)

Merging this branch to `main` publishes it. That step is the owner's.

## What is being built
1. `data-winter-2027.js`: the only place figures live (rounds: date, course, rows of name / handicap / points).
2. `winter-2027.html`: status report (design v3): kicker, title, lead, progress strip, executive summary
   (3 takeaways + 4 KPIs), Exhibit 1 standings matrix, Exhibit 2 outlook, Exhibit 3 rounds chart + winners,
   Exhibit 4 method. Every number is computed in the page from the data file.
3. `season-2027.html`: 2027 season hub linking to the Winter tournament.
4. Nav: "2027 season" link added to `<nav class="sitenav">` on every page that has one.
5. Print: no animations; `print-color-adjust: exact`; nav hidden; a page break between exhibits.
   Proof: headless Edge `--print-to-pdf` → `docs-winter-2027/winter-2027.pdf`.
6. `tools/winter_add_round.py`: adds next Sunday's round to the data file in one command.
7. `stamp.py`: `data-winter-2027.js` added to the cache-busted assets so updates are not hidden by browser caches.

## Design check (whole site)
- Who writes the same files: the GitHub Actions rewrite `data.js`, `changes.js`, `score-log.csv` and restamp
  every `*.html` with `stamp.py`. This branch does not touch `.github/`, `data.js` or `changes.js`; the winter
  data is in its own file, so the Actions cannot overwrite it. stamp.py only rewrites `src=`/`href=` hashes,
  so the new pages are safe under it.
- Names: as written in `data.js` (Tariq Javaid, Sid Amin, Imran K, Raz Shafi, Mahmood Sadiq, Shufqat Khan,
  Guftar Hussain, Yaseen Mohammed, Mansoor M, Waseem Goldenboy, Shazad Hussain). "Imran K T" = Imran K.
- Failure modes: a misspelt name would split a player in two → the add-round tool rejects names it has not
  seen before unless `--new` is given, and maps known aliases. A duplicate date is refused. Points outside
  0-60 are refused.
- Phone first: 360 px, the matrix scrolls inside its own box; the page itself never scrolls sideways.

## Owner's questions (sent to ax, not guessed)
1. **Basharat's name.** `data.js` spells him "Basharat2 Ali"; the brief says he is Basharat Ali. The page
   shows **"Basharat Ali"**. Yes / change to "Basharat2 Ali"?
2. **What changed panel.** `changes.js` is rebuilt from `score-log.csv` by the Action, so a hand-written note
   there would be wiped. Proposed: no entry there; the new page is announced by its nav link. Yes / no?
3. **Outlook projection.** Exhibit 2 projects each player's best-6 total as
   "average per round so far × 6" (only for players who can still reach 6 rounds). Yes / other rule?

## Check table (re-added by hand from the data)
Round 1, 15/11/2026: Tariq 37, Sid 34, Imran 33, Raz 32, Mahmood 25, Shufqat 22.
Round 2, 22/11/2026: Guftar 31, Yaseen 30, Mansoor 29, Imran 27, Sid 27, Waseem 27, Tariq 23, Shazad 22,
Basharat 21, Raz 20, Shufqat 18.

| Pos | Player | R1 | R2 | Best-6 total | Check |
|---|---|---|---|---|---|
| 1 | Sid Amin | 34 | 27 | 61 | 34+27 |
| T2 | Tariq Javaid | 37 | 23 | 60 | 37+23 |
| T2 | Imran K | 33 | 27 | 60 | 33+27 |
| 4 | Raz Shafi | 32 | 20 | 52 | 32+20 |
| 5 | Shufqat Khan | 22 | 18 | 40 | 22+18 |
| 6 | Guftar Hussain | – | 31 | 31 | |
| 7 | Yaseen Mohammed | – | 30 | 30 | |
| 8 | Mansoor M | – | 29 | 29 | |
| 9 | Waseem Goldenboy | – | 27 | 27 | |
| 10 | Mahmood Sadiq | 25 | – | 25 | |
| 11 | Shazad Hussain | – | 22 | 22 | |
| 12 | Basharat Ali | – | 21 | 21 | |

KPIs: leader 61 (Sid Amin); gap 1st to 2nd = 61 − 60 = 1; best single round 37 (Tariq Javaid, 15/11/2026);
players 12. Round winners: R1 Tariq Javaid 37, R2 Guftar Hussain 31. No round dropped yet (2 of 7 played).

## Status
- [ ] Stage 1 PLAN.md pushed
- [ ] Stage 2 data + page
- [ ] Stage 3 nav + season hub + tool
- [ ] Stage 4 screenshots + PDF
- [ ] Stage 5 checker → CHECK-WINTER-2027.md
