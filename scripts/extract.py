"""Extract the showcase scenes from the Folger Shakespeare texts.

Source: The Folger Shakespeare (Folger Shakespeare Library, ed. Barbara Mowat and
Paul Werstine), TEI files as packaged by DraCor: https://github.com/dracor-org/shakedracor
(tei/<play>.xml). Folger texts are licensed CC BY-NC.

Usage: python3 extract.py <path to shakedracor/tei> [scenes.json]

Each scene is written as {play, act, scene, title, source, url, first, last, items}
(first/last = Folger line numbers of the passage).
items are {"d": stage direction} or {"s": speaker, "l": [lines], "n": first Folger line number}.
Stage directions inside a speech become "[...]" lines. Prose is split at Folger's line breaks.
"""
import xml.etree.ElementTree as ET, json, re, sys

NS = '{http://www.tei-c.org/ns/1.0}'
TEI = sys.argv[1] if len(sys.argv) > 1 else '/tmp/shakedracor/tei'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'scenes.json'

# Folger slugs (file name in shakedracor = slug on folger.edu)
PLAY = {
    'macbeth': 'Macbeth', 'hamlet': 'Hamlet', 'a-midsummer-nights-dream': "A Midsummer Night's Dream",
    'the-taming-of-the-shrew': 'The Taming of the Shrew', 'richard-iii': 'Richard III',
    'coriolanus': 'Coriolanus', 'as-you-like-it': 'As You Like It', 'romeo-and-juliet': 'Romeo and Juliet',
}
# id: (play file, act, scene, location, first Folger line or None, last Folger line or None)
WANT = {
    'mac13': ('macbeth', 1, 3, 'A heath near Forres.', None, None),
    'mac32': ('macbeth', 3, 2, 'The palace.', None, None),
    'mac41': ('macbeth', 4, 1, 'A cavern. In the middle, a boiling cauldron.', None, None),
    'mac55': ('macbeth', 5, 5, 'Dunsinane. Within the castle.', None, None),
    'ham13': ('hamlet', 1, 3, "A room in Polonius' house.", None, None),
    # Our cut: "To be or not to be" (3.1.64) to the end of Ophelia's "O, what a noble mind" (3.1.174)
    'ham31': ('hamlet', 3, 1, 'A room in the castle.', '3.1.64', '3.1.174'),
    'ham34': ('hamlet', 3, 4, "The Queen's closet.", None, None),
    'ham45': ('hamlet', 4, 5, 'Elsinore. A room in the castle.', None, None),
    'ham47': ('hamlet', 4, 7, 'Another room in the castle.', None, None),
    'ham51': ('hamlet', 5, 1, 'A churchyard.', None, None),
    'ham52': ('hamlet', 5, 2, 'A hall in the castle.', None, None),
    'mnd21': ('a-midsummer-nights-dream', 2, 1, 'A wood near Athens.', None, None),
    'mnd32': ('a-midsummer-nights-dream', 3, 2, 'Another part of the wood.', None, None),
    'mnd41': ('a-midsummer-nights-dream', 4, 1, 'The same. Lysander, Demetrius, Helena and Hermia lying asleep.', None, None),
    'shr21': ('the-taming-of-the-shrew', 2, 1, "Padua. A room in Baptista's house.", None, None),
    'r312': ('richard-iii', 1, 2, 'London. Another street.', None, None),
    'cor45': ('coriolanus', 4, 5, "Antium. A hall in Aufidius's house.", None, None),
    'ayl21': ('as-you-like-it', 2, 1, 'The Forest of Arden.', None, None),
    # Our cut: Benvolio's "Good morrow, cousin" (1.1.163) to the end of the scene (1.1.247)
    'rom11': ('romeo-and-juliet', 1, 1, 'Verona. A public place.', '1.1.163', None),
    'rom13': ('romeo-and-juliet', 1, 3, "A room in Capulet's house.", None, None),
}
# Speeches flagged as cut in our version: (id, first words of the speech)
CUTS = [('ham31', 'To be or not to be')]
ROMAN = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII']


def norm(t):
    return re.sub(r'\s+', ' ', t).strip()


def speech_lines(sp):
    """Return (lines, first line number) for a <sp>, prose split at <lb>."""
    out, first, last = [], None, None

    def num(n):
        nonlocal first, last
        if n and not n.startswith('SD'):
            first = first or n
            last = n

    def walk(el):
        tag = el.tag.replace(NS, '')
        if tag == 'speaker':
            return
        if tag == 'stage':
            out.append('[' + norm(''.join(el.itertext())) + ']')
            return
        if tag == 'l':
            num(el.get('n'))
            out.append(norm(''.join(el.itertext())))
            return
        if tag == 'p':  # prose: split at line breaks
            cur = []
            if el.text: cur.append(el.text)
            for x in el:
                xt = x.tag.replace(NS, '')
                if xt == 'lb':
                    num(x.get('n'))
                    if norm(''.join(cur)): out.append(norm(''.join(cur)))
                    cur = []
                elif xt == 'stage':
                    if norm(''.join(cur)): out.append(norm(''.join(cur)))
                    cur = []
                    out.append('[' + norm(''.join(x.itertext())) + ']')
                else:
                    cur.append(''.join(x.itertext()))
                if x.tail: cur.append(x.tail)
            if norm(''.join(cur)): out.append(norm(''.join(cur)))
            return
        for x in el:  # lg, q, etc.
            walk(x)

    for x in sp:
        walk(x)
    return [l for l in out if l], first, last


def lnum(n):
    a = [int(x) for x in n.split('.')]
    return tuple(a)


out = {}
for k, (f, a, s, loc, start, end) in WANT.items():
    root = ET.parse(f'{TEI}/{f}.xml').getroot()
    act = next(d for d in root.iter(NS + 'div') if d.get('type') == 'act' and d.get('n') == str(a))
    sc = next(d for d in act if d.get('type') == 'scene' and d.get('n') == str(s))
    items, started, final = [], start is None, None
    for el in sc:
        tag = el.tag.replace(NS, '')
        if tag == 'stage':
            sn = (el.get('n') or '').replace('SD ', '')
            if end and sn and lnum(sn) > lnum(end):
                break
            if started:
                items.append({'d': norm(''.join(el.itertext()))})
        elif tag == 'sp':
            sp = norm(''.join(el.find(NS + 'speaker').itertext())) if el.find(NS + 'speaker') is not None else ''
            lines, first, last = speech_lines(el)
            if not started and first and lnum(first) >= lnum(start):
                started = True
            if not started:
                continue
            if end and first and lnum(first) > lnum(end):
                break
            if not sp:  # e.g. 'A noise within' carries no speaker: treat as a stage direction
                items.append({'d': ' '.join(lines)})
                continue
            items.append({'s': sp, 'l': lines, 'n': first})
            final = last
    for ck, words in CUTS:
        if ck == k:
            hit = [it for it in items if it.get('l') and it['l'][0].replace(',', '').startswith(words)]
            assert hit, (k, words)
            hit[0]['cut'] = True
    nums = [it['n'] for it in items if it.get('n')]
    out[k] = {
        'play': PLAY[f], 'act': a, 'scene': s, 'title': f'SCENE {ROMAN[s]}.  {loc}',
        'source': 'Folger Shakespeare',
        'url': f'https://www.folger.edu/explore/shakespeares-works/{f}/read/{a}/{s}/',
        'first': nums[0] if nums else None, 'last': final, 'items': items,
    }

json.dump(out, open(OUT, 'w'), ensure_ascii=False)

for k, v in out.items():
    c = {}
    for it in v['items']:
        if 's' in it and not it.get('cut'):
            w = sum(len(re.sub(r'\[.*?\]', '', l).split()) for l in it['l'])
            c[it['s']] = c.get(it['s'], 0) + w
    print(k, v['first'], sorted(c.items(), key=lambda x: -x[1]))
