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
    'mac11': ('macbeth', 1, 1, 'An open place.', None, None),
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
    # Our cut: Mercutio's "Nay, gentle Romeo" (1.4.13) to Benvolio's "Strike, drum" (1.4.121), with Chris's internal cuts below
    'rom14': ('romeo-and-juliet', 1, 4, 'A street.', '1.4.13', None),
    # Source for the party mosaic: the shared sonnet and the kiss (1.5.104 to 1.5.122)
    'rom15': ('romeo-and-juliet', 1, 5, "A hall in Capulet's house.", '1.5.104', '1.5.122'),
    # The balcony scene: only Juliet's "Ay me" and "O Romeo, Romeo, wherefore art thou Romeo?" are played (see KEEP_ONLY)
    'rom22': ('romeo-and-juliet', 2, 2, "Capulet's orchard.", None, None),
    # Our cut: the tomb, from Romeo's "How oft when men are at the point of death" (5.3.88)
    # to Juliet's death (5.3.175); Friar Lawrence's scene with Balthasar is marked cut
    'rom53': ('romeo-and-juliet', 5, 3, 'A churchyard; in it a monument belonging to the Capulets.', '5.3.74', '5.3.175.1'),
}
# Speeches flagged as cut in our version: (id, first words of the speech)
CUTS = [('ham31', 'To be or not to be'),
        ('rom14', 'And to sink in it'), ('rom14', 'Is love a tender thing'), ('rom14', 'If love be rough with you'),
        ('rom14', 'Come knock and enter'), ('rom14', 'A torch for me'),
        ('rom53', 'Saint Francis'), ('rom53', 'Here’s one'), ('rom53', 'Bliss be upon you'), ('rom53', 'It doth so'),
        ('rom53', 'Who is it'), ('rom53', 'Romeo.'), ('rom53', 'How long hath'), ('rom53', 'Full half'),
        ('rom53', 'Go with me'), ('rom53', 'I dare not'), ('rom53', 'Stay then'), ('rom53', 'As I did sleep'),
        ('rom53', 'Lead boy'),
        # As You Like It 2.1: only "Now, my co-mates" and Amiens's reply are played
        ('ayl21', 'Come shall we go'), ('ayl21', 'Indeed my lord'), ('ayl21', 'But what said Jaques'),
        ('ayl21', 'O yes'), ('ayl21', 'And did you leave him'), ('ayl21', 'We did my lord'),
        ('ayl21', 'Show me the place'), ('ayl21', 'I’ll bring you'),
        # Midsummer 3.2: the Titania/Bottom report and "Then fate o'errules" are cut. Oberon's
        # opening speech is split instead of cut whole, so his greeting to Puck is kept (see SPLITS)
        ('mnd32', 'My mistress with a monster'), ('mnd32', 'Then fate o’errules'),
        # Hamlet 3.4: the exit couplet goes; the scene now ends on the Queen's "No more!"
        ('ham34', 'Come sir to draw toward an end')]
# Scenes where everything is cut except the speeches beginning with these words
KEEP_ONLY = [('rom22', ['Ay me', 'O Romeo, Romeo'])]
# Speeches where only the end is kept: (id, first words of the speech, text the kept part starts with)
# Line-level cuts inside a speech: (scene, first words cut, last words cut). The cut lines stay
# visible, marked Cut, and the rest of the speech carries on.
LINE_CUTS = [
    ('ham34', 'Take thy fortune.', 'To Queen.'),
    ('ham34', 'There’s letters sealed;', 'prating knave.—'),
    ('mac32', 'Naught’s had, all’s spent,', 'Than by destruction dwell in doubtful joy.'),
    ('r312', 'Set down, set down your honorable load,', '[They set down the bier.]'),
    ('r312', 'Lo, in these windows that let forth thy life', 'I pour the helpless balm of my poor eyes.'),
    ('r312', 'Cursèd the blood that let this blood from hence.', 'Than I am made by my young lord and thee.—'),
    ('r312', '[They take up the bier.]', 'Rest you, whiles I lament King Henry’s corse.'),
    ('shr21', 'I pray you do.', 'and now, Petruchio, speak.'),
    ('cor45', 'Here I clip', 'Worthy Martius,'),
    ('mac13', 'and, when he reads', 'And poured them down before him.'),
    ('mac13', 'Only to herald thee into his sight,', 'Not pay thee.'),
    ('mac13', 'In which addition, hail, most worthy thane,', 'For it is thine.'),
    ('ham13', 'Marry, well bethought.', 'As it behooves my daughter and your honor.'),
    ('ham13', 'These blazes, daughter,', 'Than may be given you.'),
    ('mnd21', 'Swifter than the moon’s sphere.', 'Our queen and all her elves come here anon.'),
    ('mnd21', 'She never had so sweet a changeling.', 'Crowns him with flowers and makes him all her joy.'),
    ('mnd21', 'But they do square, that all their elves for fear', 'Creep into acorn cups and hide them there.'),
    ('mnd21', 'Are not you he\nThat frights', 'and they shall have good luck.'),
    ('mnd21', 'I jest to Oberon and make him smile', 'A merrier hour was never wasted there.'),
    ('mnd21', 'Why art thou here,', 'To give their bed joy and prosperity?'),
    ('mnd21', 'Didst not thou lead him through the glimmering night', 'With Ariadne and Antiopa?'),
    ('mnd21', 'By pavèd fountain or by rushy brook,', 'To dance our ringlets to the whistling wind,'),
    ('mnd21', 'Therefore the winds, piping to us in vain,', 'For lack of tread, are undistinguishable.'),
    ('mnd21', 'The human mortals want their winter here.', 'And thorough this distemperature we see'),
    ('mnd21', 'As it should pierce a hundred thousand hearts.', 'In maiden meditation, fancy-free.'),
    ('mnd21', 'Why should Titania cross her Oberon?', 'Why should Titania cross her Oberon?'),
    ('mnd21', 'And in the spicèd Indian air by night', 'As from a voyage, rich with merchandise.'),
    ('mnd21', 'If not, shun me, and I will spare your haunts.', 'If not, shun me, and I will spare your haunts.'),
    ('mnd21', 'The next thing then she, waking, looks upon', '( As I can take it with another herb),'),
    ('mnd21', 'I know a bank where the wild thyme blows,', 'Take thou some of it, and seek through this grove.'),
    ('mnd21', 'Effect it with some care, that he may prove', 'And look thou meet me ere the first cock crow.'),
    ('mnd32', 'This falls out better than I could devise.', 'This falls out better than I could devise.'),
    # Macbeth 5.5 ends on "Signifying nothing."; the Messenger's entrance goes with the report
    ('mac55', '[Enter a Messenger.]', 'Thou com’st to use thy tongue: thy story quickly.'),
]
# Everything from the start of the scene to the speech beginning with these words, stage directions included, is cut
RANGE_CUTS = [('ham34', 'Polonius hides behind the arras.'), ('cor45', 'I know thee not. Thy name?'), ('shr21', '[, to Hortensio as Litio]')]
# Everything from the speech beginning with these words to the end of the scene (or up to and including the
# speech beginning with the optional third entry) is cut
RANGE_FROM = [('ham34', 'A king of shreds and patches', 'There’s letters sealed;'), ('shr21', 'Now, Signior Petruchio'),
              # Macbeth 5.5: the Birnam Wood report and "Ring the alarum bell" are cut; "They exit." stays
              ('mac55', 'Gracious my lord', 'If thou speak’st false,')]
SPLITS = [('rom14', 'Tut', 'Come, we burn daylight'), ('rom53', 'In faith, I will', 'How oft when men are at the point of death'),
          ('mnd32', 'I wonder if Titania', 'How now, mad spirit?')]
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
    for ck, words, keep in SPLITS:
        if ck == k:
            j = next(j for j, it in enumerate(items) if it.get('l') and it['l'][0].startswith(words))
            it = items[j]
            text = '\n'.join(it['l'])
            head, tail = text.split(keep, 1)
            items[j:j + 1] = [dict(it, l=head.strip().split('\n'), cut=True), {'s': it['s'], 'l': (keep + tail).split('\n'), 'n': None}]
    for ck, start, end in LINE_CUTS:
        if ck == k:
            j = next(j for j, it in enumerate(items) if it.get('l') and start in '\n'.join(it['l']))
            it = items[j]
            text = '\n'.join(it['l'])
            a = text.index(start)
            b = text.index(end, a) + len(end)
            head, mid, tail = text[:a].strip(), text[a:b].strip(), text[b:].strip()
            parts = []
            if head:
                parts.append(dict(it, l=head.split('\n')))
            parts.append({'s': it['s'], 'l': mid.split('\n'), 'n': None if head else it.get('n'), 'cut': True})
            if tail:
                parts.append({'s': it['s'], 'l': tail.split('\n'), 'n': None})
            items[j:j + 1] = parts
    for ck, last in RANGE_CUTS:
        if ck == k:
            for it in items:
                it['cut'] = True
                if (it.get('l') and it['l'][0].startswith(last)) or (it.get('d') or '').startswith(last):
                    break
    for ck, first, *upto in RANGE_FROM:
        if ck == k:
            on = False
            for it in items:
                on = on or bool(it.get('l') and it['l'][0].startswith(first))
                if on:
                    it['cut'] = True
                    if upto and it.get('l') and it['l'][0].startswith(upto[0]):
                        break
    for ck, words in CUTS:
        if ck == k:
            hit = [it for it in items if it.get('l') and it['l'][0].replace(',', '').startswith(words)]
            assert hit, (k, words)
            hit[0]['cut'] = True
    for ck, keep in KEEP_ONLY:
        if ck == k:
            for it in items:
                if not (it.get('l') and any(it['l'][0].startswith(w) for w in keep)):
                    it['cut'] = True
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
