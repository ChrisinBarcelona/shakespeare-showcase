"""Generate the light theme from the dark CSS.
Reads the main <style> block of index.html, rewrites every colour for a light
background and writes the result into <style id="light-theme">, scoped to html.light.
Run after any CSS change:  python3 mklight.py index.html"""
import re, sys, colorsys

def clamp(x): return max(0, min(1, x))

def mapc(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
    if s < 0.18 or l > 0.97 or l < 0.03:          # neutrals
        if l < 0.02:   nl, h2, s2 = 0.968, 40/360, 0.10     # page -> warm off-white
        elif l < 0.13: nl, h2, s2 = 1.0 - (l-0.02)*0.18, 40/360, 0.08   # surfaces -> white
        elif l < 0.30: nl, h2, s2 = 0.905 - (l-0.13)*0.55, 30/360, 0.05 # borders -> soft greys
        else:
            nl = 1 - l; h2 = h; s2 = min(s, 0.06)
            if nl < 0.08: nl = 0.08                           # text -> near-black, not pure
        r2, g2, b2 = colorsys.hls_to_rgb(h2, nl, s2)
    elif l >= 0.5:                                # bright accent used on dark -> deeper version
        nl = clamp(0.30 + (l-0.5)*0.35)
        r2, g2, b2 = colorsys.hls_to_rgb(h, nl, clamp(s*0.9))
    else:                                         # dark tinted surfaces -> light tints
        nl = clamp(1 - l*0.9)
        r2, g2, b2 = colorsys.hls_to_rgb(h, max(nl, 0.88), clamp(s*0.7))
    return round(r2*255), round(g2*255), round(b2*255)

def hexfix(m):
    hx = m.group(1)
    if len(hx) in (3, 4): hx = ''.join(c*2 for c in hx[:3])
    elif len(hx) == 8: hx = hx[:6]
    r, g, b = int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16)
    return '#%02x%02x%02x' % mapc(r, g, b)

def rgbafix(m):
    parts = [p.strip() for p in m.group(2).split(',')]
    r, g, b = (int(float(x)) for x in parts[:3])
    a = parts[3] if len(parts) > 3 else None
    if (r, g, b) == (0, 0, 0) and a is not None:           # shadows / scrims stay dark
        try: af = float(a)
        except ValueError: af = 1
        return 'rgba(0,0,0,%s)' % (round(af*0.45, 3) if af < 0.5 else a)
    r2, g2, b2 = mapc(r, g, b)
    return ('rgba(%d,%d,%d,%s)' % (r2, g2, b2, a)) if a is not None else ('rgb(%d,%d,%d)' % (r2, g2, b2))

COL = re.compile(r'#([0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b')
RGB = re.compile(r'(rgba?)\(([^)]*)\)')
def fixdecls(d):
    out = []
    for decl in d.split(';'):
        if ':' not in decl: continue
        prop, val = decl.split(':', 1)
        if not (COL.search(val) or RGB.search(val) or 'white' in val or 'black' in val): continue
        if prop.strip().startswith('--') and not (COL.search(val) or RGB.search(val)): continue
        v = RGB.sub(rgbafix, COL.sub(hexfix, val))
        v = re.sub(r'\bwhite\b', '#1a1a1a', v) if prop.strip() in ('color', 'fill', 'stroke') else v
        out.append(prop.strip() + ':' + v.strip())
    return ';'.join(out)

SKIP = re.compile(r'ssign|book|\.b2|bname|bmeta|bkick|\.vol\b|\.cal\b|\.cal[mdw]\b|\.cal\.sm|fccal|firstcall|\.fc[a-z]+|op-art|poster|\.ticket')
def scope(sel):
    res = []
    for s in sel.split(','):
        s = s.strip()
        if not s or SKIP.search(s): continue
        if s.startswith(':root'): res.append('html.light' + s[5:])
        elif s.startswith('html'): res.append('html.light' + s[4:])
        else: res.append(':where(html.light) ' + s)
    return ','.join(res)

def walk(css):
    out, i, n = [], 0, len(css)
    while i < n:
        j = css.find('{', i)
        if j < 0: break
        head = css[i:j].strip()
        # find matching brace
        depth, k = 1, j+1
        while depth and k < n:
            if css[k] == '{': depth += 1
            elif css[k] == '}': depth -= 1
            k += 1
        body = css[j+1:k-1]
        i = k
        head = re.sub(r'/\*.*?\*/', '', head, flags=re.S).strip()
        if head.startswith('@media') or head.startswith('@supports'):
            inner = walk(body)
            if inner: out.append(head + '{' + inner + '}')
        elif head.startswith('@'):
            continue
        else:
            d = fixdecls(re.sub(r'/\*.*?\*/', '', body, flags=re.S))
            sc = scope(head)
            if d and sc: out.append(sc + '{' + d + '}')
    return '\n'.join(out)

p = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
s = open(p).read()
s = re.sub(r'\n?<style id="light-theme">.*?</style>', '', s, flags=re.S)
main = re.search(r'<style>(.*?)</style>', s, re.S).group(1)
light = walk(main)
extra = open('light-extra.css').read() if __import__('os').path.exists('light-extra.css') else ''
s = s.replace('</style>', '</style>\n<style id="light-theme">\n' + light + '\n' + extra + '\n</style>', 1)
open(p, 'w').write(s)
print('light rules:', light.count('{'))
