"""Crop the blue 'Explanation' section (lavender header + white content) from
examGOAL explanation screenshots and set solution_image in the Full Chapter
sections. Files matched to questions by capture TIME order.
"""
from PIL import Image
import numpy as np, os, re, json, sys

SRC = "/tmp/ex_archive"
OUT = "/app/backend/chapter_images"
BANKS = [
    ("neet-chemistry-some-basic-concepts-of-chemistry", "sbc-fc", 14),
    ("neet-physics-atoms", "atoms-fc", 12),
    ("neet-chemistry-solutions", "sol-fc", 32),
]

def tkey(f):
    if f.startswith("IMG_"):
        m = re.match(r"IMG_(\d{8})_(\d{6})", f); return m.group(1) + m.group(2)
    m = re.match(r"Screenshot_(\d{4})-(\d{2})-(\d{2})-(\d{2})-(\d{2})-(\d{2})", f)
    return "".join(m.groups())

def lav_bands(a, W, H):
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    lav = ((B >= 246) & (B - R >= 4) & (R >= 224) & (R <= 250))[:, 20:W-20].sum(axis=1)
    rows = [y for y in range(150, H) if lav[y] > (W-40)*0.5]
    bands = []
    if rows:
        s = rows[0]; p = rows[0]
        for y in rows[1:]:
            if y-p > 12: bands.append((s, p)); s = y
            p = y
        bands.append((s, p))
    return bands

def crop_box(path):
    im = Image.open(path).convert('RGB'); a = np.array(im).astype(int)
    g = np.array(im.convert('L')); H, W = g.shape
    bands = lav_bands(a, W, H)
    if not bands:
        return None, None, W, H, "no-lavender"
    expl = next((b for b in bands if b[1]-b[0] >= 16), bands[0])
    top = max(0, expl[0]-6)
    addnote = None
    for b in reversed(bands):
        if b[0] > expl[1] + 60:
            addnote = b; break
    if addnote:
        bottom = addnote[0] - 12
    else:
        wf = (g[:, 8:W-8] > 248).mean(axis=1)
        bottom = H - 240
        y = expl[1] + 25; gap = 0
        while y < H:
            if wf[y] < 0.45:
                gap += 1
                if gap > 22: bottom = y - gap + 1; break
            else:
                gap = 0
            y += 1
    return top, bottom, W, H, None

def main(mode="analyze"):
    files = sorted((f for f in os.listdir(SRC) if f.lower().endswith('.jpg')), key=tkey)
    assert len(files) == 58, len(files)
    plan = []
    for key, prefix, n in BANKS:
        for j in range(n): plan.append((key, prefix))
    per = {}; counter = {}; flags = []; mapping = []
    for i, f in enumerate(files):
        key, prefix = plan[i]
        counter[key] = counter.get(key, 0) + 1
        qno = counter[key]
        top, bottom, W, H, err = crop_box(os.path.join(SRC, f))
        mapping.append((i+1, prefix, qno, f))
        if err or top is None or bottom is None or bottom-top < 60:
            flags.append((i+1, f"{prefix}-q{qno}", err or f"top={top} bot={bottom}")); print(f"[FLAG idx{i+1}->{prefix}-q{qno}] {err} top={top} bot={bottom}"); continue
        if mode == "analyze":
            print(f"idx{i+1:2d} -> {prefix}-q{qno:<2d} H={H} crop=({top},{bottom}) h={bottom-top}")
            continue
        im = Image.open(os.path.join(SRC, f)).convert('RGB')
        name = f"{prefix}-q{qno}-sol.jpg"
        im.crop((8, top, W-8, min(H, bottom))).save(os.path.join(OUT, name), quality=88)
        per.setdefault(key, {})[qno] = name
    if mode == "write":
        for key, prefix, n in BANKS:
            bp = f"/app/backend/chapter_banks/{key}.json"
            with open(bp) as fh: data = json.load(fh)
            fc = [s for s in data["sections"] if s["topic"] == "Full Chapter"][0]
            cnt = 0
            for q in fc["questions"]:
                nm = per.get(key, {}).get(q.get("display_no"))
                if nm: q["solution_image"] = nm; cnt += 1
            with open(bp, "w") as fh: json.dump(data, fh, indent=2)
            print(f"WROTE {key}: solutions set {cnt}/{len(fc['questions'])}")
    print("FLAGS:", flags)
    return mapping

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "analyze")
