"""Recompute every part's word count in index.html from the live scripts.

Basis: words still spoken on stage — live (uncut) lines in the scripts behind the
`type:"scene"` items of the running order, resolved through SCRIPT_OF. Mosaics and
fights are excluded (they are danced, fought or whispered, not spoken), and stage
directions in [brackets] inside a speech do not count. Which speaker labels belong to
which part is read from PART_SPEAKERS in index.html, so there is one such map on the
site, not two; a part with no labels there (Oberon's Fairy) stays at nothing.

Usage: python3 tools/wordcounts.py [--write]
Without --write it only prints what would change.
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
HTML = ROOT / 'index.html'

WORD = re.compile(r"[A-Za-z’'-]+")


def part_speakers(html):
    """part id -> speaker labels, read from the page's own PART_SPEAKERS map."""
    i = html.index('const PART_SPEAKERS=')
    raw = html[i:html.index('};', i) + 1]
    return {pid.strip('"'): re.findall(r'"([^"]+)"', labels)
            for pid, labels in re.findall(r'("?[\w-]+"?):\[([^\]]*)\]', raw)}


def main():
    html = HTML.read_text(encoding='utf-8')
    i = html.index('const SCRIPTS=')
    scripts = json.loads(html[i + len('const SCRIPTS='):html.index('\n', i)].rstrip(';'))

    script_of = html[html.index('const SCRIPT_OF='):]
    script_of = dict(re.findall(r'"([\w-]+)":"(\w+)"', script_of[:script_of.index('\n')]))

    order = html[html.index('const ORDER=['):html.index('const ITEMS=')]
    keys = []
    for oid, otype in re.findall(r'\{id:"([^"]+)",type:"([^"]+)"', order):
        if otype != 'scene':
            continue
        key = script_of.get(oid, oid)
        if key in scripts and key not in keys:
            keys.append(key)

    spoken = {}
    for key in keys:
        for item in scripts[key]['items']:
            if item.get('cut') or not item.get('l'):
                continue
            n = sum(len(WORD.findall(line)) for line in item['l']
                    if not line.strip().startswith('['))
            spoken[item['s']] = spoken.get(item['s'], 0) + n

    parts = re.findall(r'\{id:"([^"]+)",ch:"[^"]*",name:"[^"]*",actor:"[^"]*",words:(\d+)\}',
                       html[html.index('const PARTS=['):html.index('const ORDER=[')])
    speakers = part_speakers(html)
    unmapped = [pid for pid, _ in parts if pid not in speakers]
    if unmapped:
        print('not in PART_SPEAKERS, counted as nothing: ' + ', '.join(unmapped))

    changed = 0
    for pid, old in parts:
        new = sum(spoken.get(label, 0) for label in speakers.get(pid, []))
        if new != int(old):
            changed += 1
            print(f'{pid:18} {old:>5} -> {new:>5}')
        if '--write' in sys.argv:
            html = re.sub(r'(\{id:"%s",ch:"[^"]*",name:"[^"]*",actor:"[^"]*",words:)\d+\}' % re.escape(pid),
                          lambda m: m.group(1) + str(new) + '}', html)
    print(f'{changed} of {len(parts)} parts differ')
    if '--write' in sys.argv:
        HTML.write_text(html, encoding='utf-8')
        print('index.html updated')
    else:
        print('(dry run: pass --write to apply)')


if __name__ == '__main__':
    main()
