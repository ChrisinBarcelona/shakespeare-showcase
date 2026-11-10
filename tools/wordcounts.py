"""Recompute every part's word count in index.html from the live scripts.

Basis: words still spoken on stage — live (uncut) lines in the script behind every
item of the running order that has one, scenes, fights and mosaics alike, resolved
through SCRIPT_OF. Words are counted the way the page's own scriptWords() counts
them: bracketed stage directions removed, then split on whitespace.

Which speaker labels belong to which part is read from PART_SPEAKERS in index.html,
so there is one such map on the site rather than two. A label may be scoped to one
script as "ham45:GENTLEMAN", which counts that speaker in that script only. A part
with no entry in PART_SPEAKERS is left alone and reported, never zeroed.

Usage: python3 tools/wordcounts.py [--write]
Without --write it only prints what would change.
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
HTML = ROOT / 'index.html'

PART_RE = re.compile(r'\{id:"([^"]+)",ch:"[^"]*",name:"[^"]*",actor:"[^"]*",words:(\d+)\}')


def one_line_const(html, name):
    i = html.index('const %s=' % name)
    return html[i + len('const %s=' % name):html.index('\n', i)].rstrip(';')


def count_words(line):
    """What the page's scriptWords() counts: no [stage directions], split on spaces."""
    return len(re.sub(r'\[.*?\]', '', line).split())


def main():
    html = HTML.read_text(encoding='utf-8')
    scripts = json.loads(one_line_const(html, 'SCRIPTS'))
    script_of = dict(re.findall(r'"([\w-]+)":"(\w+)"', one_line_const(html, 'SCRIPT_OF')))

    block = html[html.index('const PART_SPEAKERS='):]
    block = block[:block.index('};') + 1]
    speakers = {pid.strip('"'): re.findall(r'"([^"]+)"', labels)
                for pid, labels in re.findall(r'("?[\w-]+"?):\[([^\]]*)\]', block)}

    order = re.findall(r'\{id:"([^"]+)"', html[html.index('const ORDER=['):html.index('const ITEMS=')])
    keys = []
    for oid in order:
        key = script_of.get(oid)
        if key in scripts and key not in keys:
            keys.append(key)

    # spoken[(script, speaker)] and spoken[speaker] — the first for scoped labels
    spoken, anywhere = {}, {}
    for key in keys:
        for item in scripts[key]['items']:
            if item.get('cut') or not item.get('l'):
                continue
            n = sum(count_words(line) for line in item['l'])
            spoken[(key, item['s'])] = spoken.get((key, item['s']), 0) + n
            anywhere[item['s']] = anywhere.get(item['s'], 0) + n

    def total(pid):
        n = 0
        for label in speakers[pid]:
            if ':' in label:
                key, name = label.split(':', 1)
                n += spoken.get((key, name), 0)
            else:
                n += anywhere.get(label, 0)
        return n

    changed, skipped = [], []
    for pid, old in PART_RE.findall(html):
        if pid not in speakers:
            skipped.append(pid)
            continue
        new = total(pid)
        if new != int(old):
            changed.append((pid, int(old), new))
            if '--write' in sys.argv:
                html = re.sub(r'(\{id:"%s",ch:"[^"]*",name:"[^"]*",actor:"[^"]*",words:)\d+\}' % re.escape(pid),
                              lambda m: m.group(1) + str(new) + '}', html)

    for pid, old, new in changed:
        print(f'{pid:20} {old:>5} -> {new:>5}')
    if skipped:
        print('left alone, no entry in PART_SPEAKERS: ' + ', '.join(skipped))
    print(f'{len(changed)} parts differ')
    if '--write' in sys.argv:
        HTML.write_text(html, encoding='utf-8')
        print('index.html updated')
    else:
        print('(dry run: pass --write to apply)')


if __name__ == '__main__':
    main()
