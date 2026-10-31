import base64, os, random, math, json

F = "/home/claude/posters/fonts/"
def ff(name, file, weight=400, style="normal"):
    b = base64.b64encode(open(F + file, "rb").read()).decode()
    return f"@font-face{{font-family:'{name}';src:url(data:font/woff2;base64,{b}) format('woff2');font-weight:{weight};font-style:{style}}}"

FONTS = "".join([
    ff("Slab", "alfa-slab-one-latin-400-normal.woff2"),
    ff("Osw", "oswald-latin-600-normal.woff2", 600),
    ff("Osw", "oswald-latin-400-normal.woff2", 400),
    ff("Bod", "bodoni-moda-latin-400-italic.woff2", 400, "italic"),
    ff("Bod", "bodoni-moda-latin-400-normal.woff2", 400),
])

INK = "#111010"
CREAM = "#F1E4CC"

# ---------------------------------------------------------------- figures
def person(x, gy, h, kind="man", facing=1, hat=None, arm="down", prop=None, lean=0):
    r = .075 * h
    hx, hy = x, gy - h + r
    y0 = gy - h + 2 * r + .01 * h  # shoulders
    s = []
    if kind == "woman":
        s.append(f'<path d="M{x-.10*h},{y0} L{x+.10*h},{y0} L{x+.07*h},{y0+.28*h} L{x+.21*h},{gy} L{x-.21*h},{gy} L{x-.07*h},{y0+.28*h} Z"/>')
    else:
        y1 = y0 + .36 * h
        coat = y0 + .55 * h
        s.append(f'<path d="M{x-.13*h},{y0} L{x+.13*h},{y0} L{x+.12*h},{y1} L{x+.16*h},{coat} L{x+.04*h},{coat} L{x+.03*h},{gy} L{x+.11*h},{gy} L{x+.10*h},{coat} '
                 f'L{x-.02*h},{coat} L{x-.05*h},{gy} L{x-.13*h},{gy} L{x-.10*h},{coat} L{x-.16*h},{coat} L{x-.12*h},{y1} Z"/>')
    # arms
    for side in (-1, 1):
        sx = x + side * .13 * h
        if arm == "up" and side == facing:
            s.append(f'<path d="M{sx},{y0} L{sx+side*.05*h},{y0} L{sx+side*.12*h},{y0-.30*h} L{sx+side*.07*h},{y0-.31*h} Z"/>')
        elif arm == "akimbo":
            s.append(f'<path d="M{sx},{y0} L{sx+side*.13*h},{y0+.16*h} L{sx+side*.02*h},{y0+.33*h} L{sx-side*.02*h},{y0+.30*h} L{sx+side*.07*h},{y0+.17*h} L{sx-side*.02*h},{y0+.04*h} Z"/>')
        elif arm == "reach" and side == facing:
            s.append(f'<path d="M{sx},{y0} L{sx+side*.32*h},{y0+.08*h} L{sx+side*.32*h},{y0+.13*h} L{sx},{y0+.10*h} Z"/>')
        else:
            s.append(f'<path d="M{sx},{y0} L{sx+side*.04*h},{y0} L{sx+side*.07*h},{y0+.40*h} L{sx+side*.02*h},{y0+.41*h} Z"/>')
    s.append(f'<circle cx="{hx}" cy="{hy}" r="{r}"/>')
    if hat == "crown":
        cy = hy - r * .55
        s.append(f'<path d="M{hx-r},{cy} L{hx-r},{cy-r*.9} L{hx-r*.5},{cy-r*.4} L{hx},{cy-r*1.1} L{hx+r*.5},{cy-r*.4} L{hx+r},{cy-r*.9} L{hx+r},{cy} Z"/>')
    elif hat == "hat":
        s.append(f'<rect x="{hx-r*1.7}" y="{hy-r*.75}" width="{r*3.4}" height="{r*.32}"/><rect x="{hx-r*.95}" y="{hy-r*1.75}" width="{r*1.9}" height="{r*1.1}" rx="{r*.2}"/>')
    elif hat == "helmet":
        s.append(f'<path d="M{hx-r*1.15},{hy} A{r*1.15},{r*1.15} 0 0 1 {hx+r*1.15},{hy} Z"/><path d="M{hx-r*.2},{hy-r*1.1} Q{hx+r*1.6*facing},{hy-r*2.2} {hx+r*2.2*facing},{hy-r*.6} L{hx+r*.2},{hy-r*.9} Z"/>')
    elif hat == "veil":
        s.append(f'<path d="M{hx-r*1.2},{hy+r*2.5} Q{hx-r*1.4},{hy-r*1.4} {hx},{hy-r*1.3} Q{hx+r*1.4},{hy-r*1.4} {hx+r*1.2},{hy+r*2.5} Z"/>')
    if prop == "cane":
        px = x + facing * .22 * h
        s.append(f'<rect x="{px-.012*h}" y="{y0+.38*h}" width="{.024*h}" height="{gy-y0-.38*h}"/>')
    elif prop == "spear":
        px = x + facing * .19 * h
        s.append(f'<rect x="{px-.01*h}" y="{gy-1.35*h}" width="{.02*h}" height="{1.35*h}"/><path d="M{px},{gy-1.48*h} L{px+.04*h},{gy-1.33*h} L{px-.04*h},{gy-1.33*h} Z"/>')
    elif prop == "skull":
        sx = x + facing * .25 * h
        s.append(f'<circle cx="{sx}" cy="{y0-.36*h}" r="{.07*h}"/>')
    elif prop == "sword":
        px = x + facing * .2 * h
        s.append(f'<rect x="{px-.008*h}" y="{y0+.1*h}" width="{.016*h}" height="{.6*h}" transform="rotate({-25*facing} {px} {y0+.4*h})"/>')
    elif prop == "staff":
        px = x + facing * .2 * h
        s.append(f'<rect x="{px-.01*h}" y="{gy-1.15*h}" width="{.02*h}" height="{1.15*h}"/>')
    g = "".join(s)
    if lean:
        g = f'<g transform="rotate({lean} {x} {gy})">{g}<circle cx="{x-.05*h*facing}" cy="{y0+.05*h}" r="{.11*h}"/></g>'
    if facing == -1:
        g = f'<g transform="translate({2*x},0) scale(-1,1)">{g}</g>'
    return g

# ---------------------------------------------------------------- motifs (drawn in a 1080-wide space; cx center, top..bottom)
def drips(x, y, n, rnd, scale=1):
    out = ""
    for i in range(n):
        dx = x + rnd.uniform(-18, 18) * scale; dy = y + rnd.uniform(20, 150) * scale; r = rnd.uniform(6, 11) * scale
        out += f'<path d="M{dx},{dy-r*2.4} Q{dx+r},{dy-r*.4} {dx},{dy+r} Q{dx-r},{dy-r*.4} {dx},{dy-r*2.4} Z"/>'
    return out

def motif(play, cx, top, bottom, bg, rnd):
    L = bottom - top
    if play == "macbeth":   # dagger hanging point-down
        g = f'<rect x="{cx-5}" y="{top-200}" width="10" height="{200+L*.06}"/>'
        y = top + L * .06
        g += f'<circle cx="{cx}" cy="{y+22}" r="24"/>'
        g += f'<rect x="{cx-17}" y="{y+40}" width="34" height="{L*.14}" rx="8"/>'
        for i in range(5):
            g += f'<rect x="{cx-20}" y="{y+52+i*L*.026}" width="40" height="7" fill="{bg}" opacity=".35"/>'
        gy = y + 40 + L * .14
        g += f'<path d="M{cx-120},{gy} Q{cx},{gy-24} {cx+120},{gy} L{cx+128},{gy+26} Q{cx},{gy+8} {cx-128},{gy+26} Z"/>'
        bt = gy + 22
        tip = bottom - L * .12
        g += f'<path d="M{cx-34},{bt} L{cx+34},{bt} L{cx+28},{tip-90} L{cx},{tip} L{cx-28},{tip-90} Z"/>'
        g += f'<path d="M{cx-4},{bt+20} L{cx+4},{bt+20} L{cx+2},{tip-120} L{cx-2},{tip-120} Z" fill="{bg}" opacity=".55"/>'
        g += drips(cx, tip, 4, rnd, 1.1)
        return g
    if play == "hamlet":    # skull as a moon
        r = min(L * .2, 230); y = top + L * .38
        g = f'<path d="M{cx-r},{y} A{r},{r} 0 1 1 {cx+r},{y} Q{cx+r},{y+r*.55} {cx+r*.62},{y+r*.72} L{cx+r*.55},{y+r*1.12} Q{cx},{y+r*1.32} {cx-r*.55},{y+r*1.12} L{cx-r*.62},{y+r*.72} Q{cx-r},{y+r*.55} {cx-r},{y} Z"/>'
        g += f'<ellipse cx="{cx-r*.38}" cy="{y+r*.12}" rx="{r*.25}" ry="{r*.28}" fill="{bg}"/><ellipse cx="{cx+r*.38}" cy="{y+r*.12}" rx="{r*.25}" ry="{r*.28}" fill="{bg}"/>'
        g += f'<path d="M{cx},{y+r*.4} L{cx+r*.12},{y+r*.66} L{cx-r*.12},{y+r*.66} Z" fill="{bg}"/>'
        for i in range(-3, 4):
            g += f'<rect x="{cx+i*r*.13-r*.045}" y="{y+r*.86}" width="{r*.09}" height="{r*.2}" fill="{bg}"/>'
        g += f'<path d="M{cx-r*.75},{y-r*.55} Q{cx-r*.45},{y-r*.25} {cx-r*.62},{y+r*.05}" stroke="{bg}" stroke-width="7" fill="none" opacity=".6"/>'
        return g
    if play == "midsummer":  # crescent moon with hanging flower
        r = min(L * .2, 230); y = top + L * .3
        g = f'<circle cx="{cx}" cy="{y}" r="{r}"/><circle cx="{cx+r*.42}" cy="{y-r*.22}" r="{r*.86}" fill="{bg}"/>'
        for (sx, sy, s) in [(-1.6, -.6, 16), (1.5, -.9, 12), (1.9, .4, 9), (-1.9, .7, 10), (1.2, 1.3, 7)]:
            px, py = cx + sx * r, y + sy * r
            g += f'<path d="M{px},{py-s*1.8} L{px+s*.5},{py-s*.5} L{px+s*1.8},{py} L{px+s*.5},{py+s*.5} L{px},{py+s*1.8} L{px-s*.5},{py+s*.5} L{px-s*1.8},{py} L{px-s*.5},{py-s*.5} Z"/>'
        vx = cx - r * .55; vy = y + r * .85
        g += f'<path d="M{vx},{vy} C{vx+60},{vy+120} {vx-50},{vy+220} {vx+10},{bottom-L*.2}" stroke="{INK}" stroke-width="6" fill="none"/>'
        fx, fy = vx + 10, bottom - L * .2
        for a in range(5):
            ang = a * 72 - 90
            px = fx + 34 * math.cos(math.radians(ang)); py = fy + 34 * math.sin(math.radians(ang))
            g += f'<ellipse cx="{px}" cy="{py}" rx="26" ry="18" transform="rotate({ang} {px} {py})"/>'
        g += f'<circle cx="{fx}" cy="{fy}" r="13" fill="{bg}"/>'
        for (lx, ly, rot) in [(vx + 30, vy + 70, 40), (vx - 22, vy + 170, -30)]:
            g += f'<ellipse cx="{lx}" cy="{ly}" rx="30" ry="12" transform="rotate({rot} {lx} {ly})"/>'
        return g
    if play == "shrew":      # wasp on a thread
        y = top + L * .5
        g = f'<rect x="{cx-3}" y="{top-200}" width="6" height="{y-top+200-90}"/>'
        g += f'<ellipse cx="{cx-85}" cy="{y-70}" rx="95" ry="42" transform="rotate(-28 {cx-85} {y-70})" fill="{bg}" stroke="{INK}" stroke-width="10"/>'
        g += f'<ellipse cx="{cx+85}" cy="{y-70}" rx="95" ry="42" transform="rotate(28 {cx+85} {y-70})" fill="{bg}" stroke="{INK}" stroke-width="10"/>'
        g += f'<circle cx="{cx}" cy="{y-110}" r="34"/><ellipse cx="{cx}" cy="{y-50}" rx="38" ry="44"/>'
        g += f'<path d="M{cx-8},{y-140} Q{cx-40},{y-200} {cx-60},{y-190}" stroke="{INK}" stroke-width="6" fill="none"/><path d="M{cx+8},{y-140} Q{cx+40},{y-200} {cx+60},{y-190}" stroke="{INK}" stroke-width="6" fill="none"/>'
        g += f'<ellipse cx="{cx}" cy="{y+70}" rx="62" ry="100"/>'
        for i in range(3):
            g += f'<rect x="{cx-70}" y="{y+22+i*42}" width="140" height="14" fill="{bg}" transform="rotate(0)"/>'
        g += f'<path d="M{cx-18},{y+160} L{cx+18},{y+160} L{cx},{y+225} Z"/>'
        for side in (-1, 1):
            for i in range(3):
                g += f'<path d="M{cx+side*30},{y-40+i*25} L{cx+side*(80+i*10)},{y+10+i*35} L{cx+side*(70+i*10)},{y+60+i*40}" stroke="{INK}" stroke-width="6" fill="none"/>'
        return g
    if play == "richard":    # tilted crown with drips
        y = top + L * .32; w = 300
        g = f'<rect x="{cx-3}" y="{top-200}" width="6" height="{y-top+200-60}"/>'
        g += f'<g transform="rotate(-12 {cx} {y})"><path d="M{cx-w/2},{y+60} L{cx-w/2},{y-90} L{cx-w*.25},{y-10} L{cx},{y-140} L{cx+w*.25},{y-10} L{cx+w/2},{y-90} L{cx+w/2},{y+60} Z"/>'
        g += f'<rect x="{cx-w/2-8}" y="{y+40}" width="{w+16}" height="46" rx="6"/>'
        for px in (-w/2, -w*.25, 0, w*.25, w/2):
            hy = y - 90 if px in (-w/2, w/2) else (y - 140 if px == 0 else y - 10)
            g += f'<circle cx="{cx+px}" cy="{hy-14}" r="16"/>'
        g += f'<circle cx="{cx}" cy="{y+63}" r="11" fill="{"#F1E4CC"}" opacity=".0"/>'
        for px in (-w*.3, 0, w*.3):
            g += f'<circle cx="{cx+px}" cy="{y+63}" r="10" fill="{bg}"/>'
        g += "</g>"
        g += drips(cx + 10, y + 120, 6, rnd, 1.3)
        return g
    if play == "coriolanus":  # crossed swords
        y = top + L * .42; ln = L * .62
        g = ""
        for ang in (-28, 28):
            g += f'<g transform="rotate({ang} {cx} {y})"><path d="M{cx-26},{y-ln/2+70} L{cx+26},{y-ln/2+70} L{cx+22},{y+ln/2-60} L{cx},{y+ln/2} L{cx-22},{y+ln/2-60} Z"/>'
            g += f'<rect x="{cx-80}" y="{y-ln/2+44}" width="160" height="26" rx="8"/><rect x="{cx-15}" y="{y-ln/2-40}" width="30" height="86" rx="10"/><circle cx="{cx}" cy="{y-ln/2-52}" r="24"/>'
            g += f'<path d="M{cx-3},{y-ln/2+90} L{cx+3},{y-ln/2+90} L{cx+2},{y+ln/2-90} L{cx-2},{y+ln/2-90} Z" fill="{bg}" opacity=".55"/></g>'
        return g
    if play == "ayli":       # great oak on the horizon (drawn from bottom)
        tb = bottom; th = L * .78
        g = f'<path d="M{cx-38},{tb} Q{cx-30},{tb-th*.4} {cx-12},{tb-th*.55} L{cx+12},{tb-th*.55} Q{cx+30},{tb-th*.4} {cx+38},{tb} Z"/>'
        g += f'<path d="M{cx-14},{tb-th*.45} Q{cx-120},{tb-th*.6} {cx-190},{tb-th*.58}" stroke="{INK}" stroke-width="22" fill="none"/>'
        g += f'<path d="M{cx+14},{tb-th*.5} Q{cx+120},{tb-th*.66} {cx+200},{tb-th*.62}" stroke="{INK}" stroke-width="20" fill="none"/>'
        for (dx, dy, r) in [(0, .78, 150), (-150, .66, 120), (150, .68, 125), (-240, .56, 90), (240, .57, 92), (-80, .9, 110), (90, .9, 112), (0, .98, 95), (-200, .78, 95), (200, .8, 98)]:
            g += f'<circle cx="{cx+dx}" cy="{tb-th*dy}" r="{r}"/>'
        for i in range(26):
            px = cx + rnd.uniform(-300, 300); py = tb - th * rnd.uniform(.55, 1.02)
            g += f'<ellipse cx="{px}" cy="{py}" rx="16" ry="8" transform="rotate({rnd.uniform(0,180)} {px} {py})"/>'
        return g
    if play == "all":        # garland of the seven emblems on a thread
        g = f'<rect x="{cx-4}" y="{top-200}" width="8" height="{L+200-L*.08}"/>'
        icons = ["dagger", "skull", "moon", "wasp", "crown", "swords", "leaf"]
        step = (L * .86) / len(icons)
        for i, ic in enumerate(icons):
            y = top + step * (i + .5); s = min(step * .42, 70)
            if ic == "dagger":
                g += f'<circle cx="{cx}" cy="{y-s}" r="{s*.25}"/><path d="M{cx-s*.9},{y-s*.55} L{cx+s*.9},{y-s*.55} L{cx+s*.9},{y-s*.35} L{cx-s*.9},{y-s*.35} Z"/><path d="M{cx-s*.22},{y-s*.35} L{cx+s*.22},{y-s*.35} L{cx},{y+s*1.1} Z"/>'
            elif ic == "skull":
                g += f'<circle cx="{cx}" cy="{y-s*.1}" r="{s*.75}"/><rect x="{cx-s*.42}" y="{y+s*.3}" width="{s*.84}" height="{s*.55}" rx="{s*.1}"/><circle cx="{cx-s*.28}" cy="{y-s*.05}" r="{s*.2}" fill="{bg}"/><circle cx="{cx+s*.28}" cy="{y-s*.05}" r="{s*.2}" fill="{bg}"/>'
            elif ic == "moon":
                g += f'<circle cx="{cx}" cy="{y}" r="{s*.9}"/><circle cx="{cx+s*.4}" cy="{y-s*.2}" r="{s*.75}" fill="{bg}"/>'
            elif ic == "wasp":
                g += f'<ellipse cx="{cx-s*.55}" cy="{y-s*.5}" rx="{s*.55}" ry="{s*.25}" transform="rotate(-25 {cx-s*.55} {y-s*.5})"/><ellipse cx="{cx+s*.55}" cy="{y-s*.5}" rx="{s*.55}" ry="{s*.25}" transform="rotate(25 {cx+s*.55} {y-s*.5})"/><ellipse cx="{cx}" cy="{y+s*.2}" rx="{s*.38}" ry="{s*.75}"/><rect x="{cx-s*.4}" y="{y+s*.05}" width="{s*.8}" height="{s*.12}" fill="{bg}"/><rect x="{cx-s*.4}" y="{y+s*.38}" width="{s*.8}" height="{s*.12}" fill="{bg}"/>'
            elif ic == "crown":
                g += f'<path d="M{cx-s},{y+s*.5} L{cx-s},{y-s*.5} L{cx-s*.5},{y} L{cx},{y-s*.8} L{cx+s*.5},{y} L{cx+s},{y-s*.5} L{cx+s},{y+s*.5} Z"/>'
            elif ic == "swords":
                for a in (-30, 30):
                    g += f'<rect x="{cx-s*.09}" y="{y-s*1.05}" width="{s*.18}" height="{s*2.1}" transform="rotate({a} {cx} {y})"/><rect x="{cx-s*.45}" y="{y-s*.75}" width="{s*.9}" height="{s*.14}" transform="rotate({a} {cx} {y})"/>'
            elif ic == "leaf":
                g += f'<path d="M{cx},{y-s} Q{cx+s*1.1},{y} {cx},{y+s*1.1} Q{cx-s*1.1},{y} {cx},{y-s} Z"/><rect x="{cx-3}" y="{y+s*.9}" width="6" height="{s*.5}"/>'
        return g
    return ""

FIGS = {
    "macbeth": lambda gy, h: person(470, gy, h, "man", 1, "crown") + person(590, gy, h * .92, "woman", -1),
    "hamlet": lambda gy, h: person(480, gy, h, "man", 1, None, "up", "skull") + person(600, gy, h * .96, "man", -1, "hat"),
    "midsummer": lambda gy, h: person(380, gy, h * .8, "woman", 1, None, "reach") + person(480, gy, h * .82, "man", 1, None, "reach") + person(580, gy, h * .78, "woman", 1, None, "reach") + person(690, gy, h * .82, "man", -1, None, "reach"),
    "shrew": lambda gy, h: person(470, gy, h, "man", 1, "hat", "akimbo") + person(610, gy, h * .92, "woman", -1, None, "akimbo"),
    "richard": lambda gy, h: person(470, gy, h * .92, "man", 1, "crown", "down", "cane", lean=8) + person(610, gy, h * .92, "woman", -1, "veil"),
    "coriolanus": lambda gy, h: person(450, gy, h, "man", 1, "helmet", "down", "spear") + person(630, gy, h, "man", -1, "helmet", "down", "spear"),
    "ayli": lambda gy, h: person(400, gy, h * .7, "man", 1, "hat", "down", "staff") + person(690, gy, h * .7, "man", -1),
    "all": lambda gy, h: "".join(person(240 + i * 100, gy, h * (.9 + .1 * ((i * 37) % 3) / 2), "woman" if i in (1, 4) else "man", 1 if i < 3 else -1,
                                        ["crown", None, "hat", None, "veil", "helmet", "hat"][i]) for i in range(7)),
}

POSTERS = [
    # id, play-key, bg, title lines, quote, cite, title size
    ("macbeth", "macbeth", "#D8432A", ["MACBETH"], "Fair is foul, and foul is fair.", "Macbeth, I.i"),
    ("hamlet", "hamlet", "#7FA2BE", ["HAMLET"], "Alas, poor Yorick!", "Hamlet, V.i"),
    ("midsummer", "midsummer", "#86B566", ["A MIDSUMMER", "NIGHT'S DREAM"], "Lord, what fools these mortals be!", "A Midsummer Night's Dream, III.ii"),
    ("shrew", "shrew", "#E5A92A", ["THE TAMING", "OF THE SHREW"], "If I be waspish, best beware my sting.", "The Taming of the Shrew, II.i"),
    ("richard", "richard", "#9461BE", ["RICHARD III"], "Was ever woman in this humour wooed?", "Richard III, I.ii"),
    ("coriolanus", "coriolanus", "#D9822B", ["CORIOLANUS"], "There is a world elsewhere.", "Coriolanus, III.iii"),
    ("ayli", "ayli", "#B9B45A", ["AS YOU", "LIKE IT"], "Sweet are the uses of adversity.", "As You Like It, II.i"),
    ("company", "all", "#D8432A", ["SHAKESPEARE"], "All the world's a stage.", "As You Like It, II.vii"),
]

def grass(y, rnd, W):
    pts = [f"M0,{y}"]
    x = 0
    while x < W:
        x += rnd.uniform(5, 14)
        pts.append(f"L{x:.1f},{y - rnd.uniform(4, 26):.1f}")
        x += rnd.uniform(3, 9)
        pts.append(f"L{x:.1f},{y + rnd.uniform(0, 4):.1f}")
    return " ".join(pts) + f" L{W},{y+60} L0,{y+60} Z"

def poster(p, W, H):
    pid, key, bg, lines, quote, cite = p
    rnd = random.Random(pid + str(H))
    ground = H * (.645 if H < 1500 else .64)
    tall = H > 1500
    figh = 150 if not tall else 175
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
           '<defs><filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.2 1.05"/></filter>',
           '<filter id="worn"><feTurbulence type="fractalNoise" baseFrequency="1.4" numOctaves="1" seed="9" result="n"/><feColorMatrix in="n" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -16 13" result="m"/><feComposite in="SourceGraphic" in2="m" operator="in"/></filter>',
           f'<radialGradient id="vig" cx=".5" cy=".38" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".28"/></radialGradient></defs>',
           f'<rect width="{W}" height="{H}" fill="{bg}"/>',
           f'<g fill="{INK}">{motif(key, W/2, 0 if key not in ("hamlet","midsummer","ayli") else H*.05, ground - figh - 20 if key != "ayli" else ground+8, bg, rnd)}</g>',
           f'<g fill="{INK}">{FIGS[key](ground + 6, figh)}</g>',
           f'<path d="{grass(ground, rnd, W)}" fill="{INK}"/><rect y="{ground+40}" width="{W}" height="{H-ground}" fill="{INK}"/>',
           f'<rect width="{W}" height="{H}" fill="url(#vig)"/>']
    # text block
    y = ground + (78 if not tall else 120)
    svg.append(f'<text x="{W/2}" y="{y}" text-anchor="middle" font-family="Osw" font-weight="600" font-size="30" letter-spacing="6" fill="{CREAM}">A CHRIS KELLY PRODUCTION</text>')
    longest = max(len(l) for l in lines)
    cap = (175 if len(lines) == 1 else 112) * (1.12 if tall else 1)
    size = min(cap, (W - 120) / (longest * .80))
    y += size * .9 + 14
    for l in lines:
        svg.append(f'<text x="{W/2}" y="{y}" text-anchor="middle" font-family="Slab" font-size="{size:.0f}" fill="{CREAM}" filter="url(#worn)">{l}</text>')
        y += size * 1.0
    y += 50 - size * 1.0 + (30 if tall else 0)
    svg.append(f'<text x="{W/2}" y="{y}" text-anchor="middle" font-family="Bod" font-style="italic" font-size="{36 if not tall else 42}" fill="{CREAM}">“{quote}”</text>')
    y += 36
    svg.append(f'<text x="{W/2}" y="{y}" text-anchor="middle" font-family="Osw" font-weight="400" font-size="18" letter-spacing="5" fill="{bg}">{cite.upper()}</text>')
    by = H - (52 if not tall else 110)
    if tall:
        svg.append(f'<text x="{W/2}" y="{by-46}" text-anchor="middle" font-family="Osw" font-weight="600" font-size="38" letter-spacing="4" fill="{CREAM}">TEATRE GAUDÍ · MARCH 2027</text>')
        svg.append(f'<text x="{W/2}" y="{by}" text-anchor="middle" font-family="Osw" font-weight="400" font-size="26" letter-spacing="4" fill="{CREAM}" opacity=".8">THURSDAYS · FRIDAYS · SATURDAYS · CURTAIN 20:00</text>')
    else:
        svg.append(f'<line x1="{W/2-60}" y1="{by-44}" x2="{W/2+60}" y2="{by-44}" stroke="{CREAM}" stroke-opacity=".35"/>')
        svg.append(f'<text x="{W/2}" y="{by}" text-anchor="middle" font-family="Osw" font-weight="600" font-size="24" letter-spacing="4" fill="{CREAM}" opacity=".9">TEATRE GAUDÍ · THU–SAT IN MARCH 2027 · CURTAIN 20:00</text>')
    svg.append(f'<rect width="{W}" height="{H}" filter="url(#grain)" opacity=".16"/>')
    svg.append("</svg>")
    return "".join(svg)

def ticket():
    W, H = 1600, 620
    bg = "#D8432A"
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         '<defs><filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.2 1.05"/></filter>',
         '<filter id="worn"><feTurbulence type="fractalNoise" baseFrequency="1.4" numOctaves="1" seed="9" result="n"/><feColorMatrix in="n" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -16 13" result="m"/><feComposite in="SourceGraphic" in2="m" operator="in"/></filter>',
         '<mask id="notch"><rect width="1600" height="620" fill="#fff"/><circle cx="1180" cy="0" r="34" fill="#000"/><circle cx="1180" cy="620" r="34" fill="#000"/></mask></defs>',
         f'<g mask="url(#notch)"><rect width="{W}" height="{H}" fill="{bg}"/>',
         f'<rect x="0" y="420" width="1180" height="200" fill="{INK}"/>',
         f'<g fill="{INK}">{motif("all", 1100, 20, 400, bg, random.Random(3))}</g>',
         f'<text x="70" y="110" font-family="Osw" font-weight="600" font-size="30" letter-spacing="5" fill="{INK}">A CHRIS KELLY PRODUCTION</text>',
         f'<text x="64" y="270" font-family="Slab" font-size="104" fill="{INK}">SHAKESPEARE</text>',
         f'<text x="70" y="370" font-family="Bod" font-style="italic" font-size="40" fill="{INK}">“All the world\'s a stage.”</text>',
         f'<text x="70" y="490" font-family="Osw" font-weight="600" font-size="30" letter-spacing="3" fill="{CREAM}">TEATRE GAUDÍ · C/ SANT ANTONI MARIA CLARET, 120</text>',
         f'<text x="70" y="540" font-family="Osw" font-weight="400" font-size="26" letter-spacing="3" fill="{CREAM}" opacity=".85">DATE ________  ·  DOORS 19:30  ·  CURTAIN 20:00</text>',
         f'<line x1="1180" y1="40" x2="1180" y2="580" stroke="{INK}" stroke-width="4" stroke-dasharray="14 12"/>',
         f'<rect x="1180" y="0" width="420" height="620" fill="{INK}"/>',
         f'<text x="1390" y="150" text-anchor="middle" font-family="Osw" font-weight="600" font-size="34" letter-spacing="8" fill="{CREAM}">ADMIT ONE</text>',
         f'<text x="1390" y="330" text-anchor="middle" font-family="Slab" font-size="84" fill="{bg}" filter="url(#worn)">Nº 001</text>',
         f'<text x="1390" y="430" text-anchor="middle" font-family="Osw" font-weight="400" font-size="26" letter-spacing="4" fill="{CREAM}">ROW ___   SEAT ___</text>',
         f'<text x="1390" y="520" text-anchor="middle" font-family="Osw" font-weight="400" font-size="22" letter-spacing="4" fill="{CREAM}" opacity=".7">MARCH 2027 · THU–SAT</text>',
         f'<rect width="{W}" height="{H}" filter="url(#grain)" opacity=".16"/></g></svg>']
    return "".join(s)

os.makedirs("/home/claude/posters/html", exist_ok=True)
jobs = []
for p in POSTERS:
    for (W, H, tag) in [(1080, 1350, "ig"), (1080, 1920, "story")]:
        name = f"{p[0]}-{tag}"
        open(f"/home/claude/posters/html/{name}.html", "w").write(f"<!doctype html><html><head><style>{FONTS}html,body{{margin:0;background:#000}}</style></head><body>{poster(p, W, H)}</body></html>")
        jobs.append([name, W, H])
open("/home/claude/posters/html/ticket.html", "w").write(f"<!doctype html><html><head><style>{FONTS}html,body{{margin:0}}</style></head><body>{ticket()}</body></html>")
jobs.append(["ticket", 1600, 620])
json.dump(jobs, open("/home/claude/posters/jobs.json", "w"))
print(len(jobs))
