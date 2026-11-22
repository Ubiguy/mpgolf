"""Add one Sunday's round to data-winter-2027.js in one step.

    python tools/winter_add_round.py 29/11/2026 "Sid Amin 12 34" "Imran K T 10 31" ...
    python tools/winter_add_round.py 29/11/2026 --file round.txt      (one "Name Hcp Points" per line)
    add --dry-run to see the block without writing; --new "Name" to allow a first-time player.

Each player is "Name Handicap Points", as Golf GameBook shows them (Stableford NET points).
The page recalculates itself from the file: nothing else needs editing.

Guards: the date must be one of the seven winter Sundays and not already entered; points 0-60;
handicap 0-54; no player twice in a round; a name never seen before in the winter or in data.js
is refused unless passed with --new (so a typo cannot split one player into two).
Known GameBook spellings are mapped: "Imran K T" -> "Imran K", "Basharat2 Ali" -> "Basharat Ali".
"""
import argparse, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data-winter-2027.js')
ALIASES = {'Imran K T': 'Imran K', 'Basharat2 Ali': 'Basharat Ali'}


def known_names(src):
    names = set(re.findall(r"\['([^']+)',\s*\d+,\s*\d+\]", src))
    try:
        main = open(os.path.join(ROOT, 'data.js'), encoding='utf-8').read()
        names |= set(re.findall(r"'([A-Z][A-Za-z0-9]+(?: [A-Z][A-Za-z0-9]*)+)'", main))
    except OSError:
        pass
    return {ALIASES.get(n, n) for n in names}


def parse(line):
    m = re.match(r'^\s*(.+?)\s+(\d{1,2})\s+(\d{1,2})\s*$', line)
    if not m:
        sys.exit('Cannot read "%s": expected "Name Handicap Points"' % line.strip())
    name = ALIASES.get(m.group(1).strip(), m.group(1).strip())
    return name, int(m.group(2)), int(m.group(3))


def build(src, date, lines, new=()):
    dates = re.search(r'dates:\s*\[([^\]]*)\]', src).group(1)
    if "'%s'" % date not in dates:
        sys.exit('%s is not one of the winter Sundays: %s' % (date, dates))
    if re.search(r"\{\s*date:\s*'%s'" % re.escape(date), src):
        sys.exit('%s is already in the file. Edit that block by hand to correct it.' % date)
    known, rows, seen = known_names(src), [], set()
    for ln in lines:
        if not ln.strip():
            continue
        name, hcp, pts = parse(ln)
        if not 0 <= pts <= 60 or not 0 <= hcp <= 54:
            sys.exit('%s: handicap %d / points %d look wrong' % (name, hcp, pts))
        if name in seen:
            sys.exit('%s appears twice' % name)
        if name not in known and name not in new:
            sys.exit('"%s" is a new name. Check the spelling, or pass --new "%s".' % (name, name))
        seen.add(name)
        rows.append((name, hcp, pts))
    if not rows:
        sys.exit('No players given.')
    rows.sort(key=lambda r: (-r[2], r[0]))
    block = "    { date: '%s', course: 'Wike Ridge', rows: [\n%s\n    ]},\n" % (
        date, '\n'.join("      ['%s', %d, %d]," % r for r in rows))
    end = src.rindex('  ]\n};')
    return src[:end] + block + src[end:], block


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('date')
    ap.add_argument('players', nargs='*')
    ap.add_argument('--file')
    ap.add_argument('--new', action='append', default=[])
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    lines = list(a.players)
    if a.file:
        lines += open(a.file, encoding='utf-8').read().splitlines()
    src = open(DATA, encoding='utf-8').read()
    out, block = build(src, a.date, lines, set(a.new))
    print(block)
    if a.dry_run:
        print('(dry run: nothing written)')
        return
    open(DATA, 'w', encoding='utf-8', newline='\n').write(out)
    print('Added to data-winter-2027.js. Commit and push; the page updates itself.')


if __name__ == '__main__':
    main()
