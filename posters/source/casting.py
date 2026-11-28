# Casting workshop posters (Instagram 1080x1350 + Stories 1080x1920) in the Selected Works design.
# Reuses the drawing helpers from gen.py. Usage: python3 casting.py <fonts dir> <out dir>
import os, sys, json, random
SRC = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen.py")).read().split("os.makedirs(")[0]
exec(SRC)

DATE = "Saturday 19 December"
TIME = "9:30 – 12:00"
PLACE = "Centre Cultural Albareda"
ADDR = "C/ Albareda 22–24 · Poble-sec"
PARTS = [  # play, parts we're casting
    ("Macbeth", ["Macbeth", "Witches", "Ross", "Angus", "Servant"]),
    ("Hamlet", ["Claudius", "Horatio", "Gravedigger", "Other Gravemaker", "Osric", "Fortinbras", "Priest"]),
    ("Midsummer", ["Oberon", "Titania", "Puck", "Mustardseed", "Fairies", "Demetrius", "Lysander"]),
    ("The Shrew", ["Katherine", "Petruchio"]),
    ("Richard III", ["Richard III", "Queen Anne"]),
    ("Coriolanus", ["Coriolanus", "Tullus Aufidius"]),
    ("As You Like It", ["Duke Senior", "Amiens"]),
    ("Romeo & Juliet", ["Romeo", "Juliet", "Nurse"]),
    ("Crew", ["Assistant Producer"]),
]

def company(gy, h):
    out = ""
    for i in range(7):
        f = person(240 + i * 100, gy, h * (.9 + .1 * ((i * 37) % 3) / 2), "woman" if i in (1, 4) else "man", 1 if i < 3 else -1,
                   ["crown", None, "hat", None, "veil", "helmet", "hat"][i])
        # the empty place in the company: a ghost figure
        out += f'<g opacity=".28">{f}</g>' if i == 3 else f
    return out

def wrapw(words, face, size, width, sep=" · "):
    lines, cur = [], ""
    for w in words:
        t = (cur + sep + w) if cur else w
        if measure(t, face, size) > width and cur: lines.append(cur); cur = w
        else: cur = t
    lines.append(cur)
    # no orphans: if the last line is a single part, take one more down with it
    if len(lines) > 1 and " · " not in lines[-1] and " · " in lines[-2]:
        a, b = lines[-2].rsplit(" · ", 1); lines[-2:] = [a, b + sep + lines[-1]]
    return lines

def casting(W, H):
    tall = H > 1500
    k = 1.12 if tall else 1
    rnd = random.Random("casting" + str(H))
    bg = "#D8432A"
    ground = 400 if tall else 290
    figh = 130 if tall else 84
    M = 80; TW = W - 2 * M
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         '<defs><filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.2 1.05"/></filter>',
         '<radialGradient id="vig" cx=".5" cy=".38" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".28"/></radialGradient></defs>',
         f'<rect width="{W}" height="{H}" fill="{bg}"/>',
         f'<g fill="{INK}">{motif("all", W/2, 40 if tall else 0, ground - figh - 20, bg, rnd)}</g>',
         f'<g fill="{INK}">{company(ground + 6, figh)}</g>',
         f'<path d="{grass(ground, rnd, W)}" fill="{INK}"/><rect y="{ground+40}" width="{W}" height="{H-ground}" fill="{INK}"/>',
         f'<rect width="{W}" height="{H}" fill="url(#vig)"/>']
    y = ground + (110 if tall else 84)
    ks = round(24 * k)
    s.append(f'<text x="{M}" y="{y}" font-family="Inter" font-weight="600" font-size="{ks}" fill="{GREY}">A CHRIS KELLY PRODUCTION</text>')
    s1 = fit("Open Casting Workshop", (136 if tall else 112), TW)
    y += s1 * .92 + 8
    s.append(f'<text x="{M-s1*.04:.0f}" y="{y:.0f}" font-family="Tight" font-weight="600" font-size="{s1:.0f}" letter-spacing="{-s1*.045:.1f}" fill="{WHITE}">Open Casting Workshop</text>')
    s2 = fit("for Selected Works of Shakespeare", (62 if tall else 52), TW)
    y += s2 * 1.15
    s.append(f'<text x="{M-s2*.04:.0f}" y="{y:.0f}" font-family="Tight" font-weight="600" font-size="{s2:.0f}" letter-spacing="{-s2*.045:.1f}" fill="{GREY}">for Selected Works of Shakespeare</text>')
    ins = round(28 * k) if tall else 25
    y += ins * 1.9
    s.append(f'<text x="{M}" y="{y:.0f}" font-family="Inter" font-weight="500" font-size="{ins}" fill="{WHITE}" fill-opacity=".85">An English-language theatre piece · 8-show run · April 2027</text>')
    # when and where
    ds = round(34 * k) if tall else 30
    y += ds * 1.75
    s.append(f'<text x="{M}" y="{y:.0f}" font-family="Inter" font-weight="600" font-size="{ds}" fill="{WHITE}">{DATE} <tspan fill="{bg}">·</tspan> {TIME}</text>')
    y += ds * 1.35
    s.append(f'<text x="{M}" y="{y:.0f}" font-family="Inter" font-weight="500" font-size="{round(ds*.8)}" fill="{GREY}">{esc(PLACE)} · {esc(ADDR)}</text>')
    # parts
    y += ds * 1.25
    s.append(f'<line x1="{M}" y1="{y:.0f}" x2="{W-M}" y2="{y:.0f}" stroke="{WHITE}" stroke-opacity=".14" stroke-width="2"/>')
    ls = round(22 * k)
    y += ls * 2.2
    s.append(f'<text x="{M}" y="{y:.0f}" font-family="Inter" font-weight="600" font-size="{ls}" fill="{GREY}" letter-spacing="1.5">PARTS WE’RE LOOKING FOR</text>')
    ps = round(26 * k) if tall else 24; col = 200 if tall else 180
    y += ps * 1.9
    for play, parts in PARTS:
        s.append(f'<text x="{M}" y="{y:.0f}" font-family="Inter" font-weight="600" font-size="{round(ps*.82)}" fill="{GREY}">{esc(play)}</text>')
        for line in wrapw(parts, "Inter500", ps, TW - col):
            s.append(f'<text x="{M+col}" y="{y:.0f}" font-family="Inter" font-weight="500" font-size="{ps}" fill="{WHITE}">{esc(line).replace(" · ", f" <tspan fill=\'{GREY}\'>·</tspan> ")}</text>')
            y += ps * 1.36
        y += ps * .25
    if tall:
        qs = 34
        y += qs * 1.6
        s.append(f'<text x="{M}" y="{y:.0f}" font-family="Inter" font-style="italic" font-size="{qs}" fill="{WHITE}" fill-opacity=".88">“We know what we are, but know not what we may be.”</text>')
        y += qs * 1.3
        s.append(f'<text x="{M}" y="{y:.0f}" font-family="Inter" font-weight="500" font-size="{round(qs*.66)}" fill="{GREY}">Hamlet, IV.v</text>')
    # footer
    fs = round(28 * k)
    by = H - (220 if tall else 56)
    s.append(f'<line x1="{M}" y1="{by-fs-32}" x2="{W-M}" y2="{by-fs-32}" stroke="{WHITE}" stroke-opacity=".14" stroke-width="2"/>')
    s.append(f'<text x="{M}" y="{by}" font-family="Inter" font-weight="600" font-size="{fs}" fill="{WHITE}">Starts 9:30 sharp · Apply at shakespeareshow.actor</text>' if not tall else
             f'<text x="{M}" y="{by}" font-family="Inter" font-weight="600" font-size="{fs}" fill="{WHITE}">Starts 9:30 sharp</text>')
    if tall:
        s.append(f'<text x="{W-M}" y="{by}" text-anchor="end" font-family="Inter" font-weight="500" font-size="{fs-4}" fill="{GREY}">shakespeareshow.actor</text>')
    s.append(f'<rect width="{W}" height="{H}" filter="url(#grain)" opacity=".12"/></svg>')
    return "".join(s), y, by

os.makedirs(os.path.join(OUT, "html"), exist_ok=True)
jobs = []
for (W, H, t) in [(1080, 1350, "ig"), (1080, 1920, "story")]:
    svg, ytext, yfoot = casting(W, H)
    print(t, "text ends", round(ytext), "footer", yfoot)
    open(os.path.join(OUT, "html", f"casting-{t}.html"), "w").write(f"<!doctype html><html><head><meta charset='utf-8'><style>{FONTS}html,body{{margin:0;background:#000}}</style></head><body>{svg}</body></html>")
    jobs.append([f"casting-{t}", W, H])
json.dump(jobs, open(os.path.join(OUT, "jobs.json"), "w"))
