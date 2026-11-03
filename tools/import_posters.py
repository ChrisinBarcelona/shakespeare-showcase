"""Import the final posters exported from Figma into the site.

Usage: python3 tools/import_posters.py <folder of PNG exports>

Each Figma frame (1190x1684) is fitted onto the site's two formats by
extending its own flat background colour, so nothing is cropped:
  - Instagram 4:5   1080x1350  -> posters/jpg/<key>-ig.jpg
  - TikTok/Stories  1080x1920  -> posters/jpg/<key>-story.jpg
plus 540px-wide thumbnails in posters/thumb/.
"""
import os, re, sys
from PIL import Image

NAMES = {  # Figma frame name (after "Final — ") -> site key
    "love": "love", "power": "power", "madness": "madness", "hate": "hate",
    "selected-works (template)": "company", "selected-works": "company",
    "macbeth": "macbeth", "weird-sisters-a": "witches", "weird-sisters-b": "witches-b",
    "hamlet": "hamlet", "midsummer": "midsummer", "shrew": "shrew",
    "richard": "richard", "coriolanus": "coriolanus", "ayli": "ayli",
}
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FULL, THUMB = os.path.join(ROOT, "posters/jpg"), os.path.join(ROOT, "posters/thumb")


def key_for(fname):
    stem = os.path.splitext(os.path.basename(fname))[0]
    stem = re.sub(r"^Final\s*[—–-]\s*", "", stem).strip().lower()
    stem = re.sub(r"\s*\(\d+\)$", "", stem)  # "name (1)" duplicates from exports
    return NAMES.get(stem)


def fit(src, W, H):
    if W / H > src.width / src.height:
        # Instagram 4:5 is wider than the A-ratio poster. Trim only the empty
        # slivers of top/bottom margin, then extend the sides by mirroring the
        # poster's own edge, so full-bleed artwork (skull, boar, branches) carries
        # on instead of stopping at a hard line. Text sits further in than the band.
        src = src.crop((0, round(src.height * .027), src.width, round(src.height * .995)))
        s = H / src.height
        img = src.resize((round(src.width * s), H), Image.LANCZOS)
        pad = (W - img.width) // 2
        out = Image.new("RGB", (W, H))
        out.paste(img, (pad, 0))
        out.paste(img.crop((0, 0, pad, H)).transpose(Image.FLIP_LEFT_RIGHT), (0, 0))
        r = W - pad - img.width
        out.paste(img.crop((img.width - r, 0, img.width, H)).transpose(Image.FLIP_LEFT_RIGHT), (pad + img.width, 0))
        return out
    bg = src.getpixel((4, 4))
    s = min(W / src.width, H / src.height)
    img = src.resize((round(src.width * s), round(src.height * s)), Image.LANCZOS)
    out = Image.new("RGB", (W, H), bg)
    out.paste(img, ((W - img.width) // 2, (H - img.height) // 2))
    return out


def main(folder):
    done = {}
    for f in sorted(os.listdir(folder)):
        if not f.lower().endswith((".png", ".jpg", ".jpeg")):
            continue
        k = key_for(f)
        if not k:
            print("skip (unknown name):", f)
            continue
        src = Image.open(os.path.join(folder, f)).convert("RGB")
        for tag, (W, H) in {"ig": (1080, 1350), "story": (1080, 1920)}.items():
            out = fit(src, W, H)
            out.save(os.path.join(FULL, f"{k}-{tag}.jpg"), quality=90, optimize=True, progressive=True)
            out.resize((540, H * 540 // W), Image.LANCZOS).save(
                os.path.join(THUMB, f"{k}-{tag}.jpg"), quality=82, optimize=True, progressive=True)
        done[k] = f
        print(f"{k:11s} <- {f}")
    print(len(done), "posters imported")


if __name__ == "__main__":
    main(sys.argv[1])
