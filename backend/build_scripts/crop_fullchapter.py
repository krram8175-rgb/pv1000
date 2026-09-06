"""Crop examGOAL-style screenshots (blue A/B/C/D circles, card layout) into
question + option images, and populate the 'Full Chapter' sections of
Some Basic Concepts of Chemistry (14), Atoms (12), Solutions (32).
Capture order across 58 files -> banks in that order.
"""
from PIL import Image
import numpy as np, os, json, sys

SRC = "/tmp/fc_archive"
OUT = "/app/backend/chapter_images"

BANKS = [
    ("neet-chemistry-some-basic-concepts-of-chemistry", "sbc-fc", 14),
    ("neet-physics-atoms", "atoms-fc", 12),
    ("neet-chemistry-solutions", "sol-fc", 32),
]

# hardcoded overrides for the 3 tricky images (indices in the sorted list)
OVERRIDE = {
    0:  {"q": (466, 1401), "opts": [(1434, 1579), (1628, 1773), (1822, 1967)]},           # table, D cut off
    12: {"q": (446, 486),  "opts": [(512, 615), (650, 753), (789, 891), (927, 1029)]},     # browser-view variant
    17: {"q": (466, 676),  "opts": [(709, 854), (903, 1048), (1097, 1242), (1291, 1436)]}, # D circle occluded
    33: {"q": (466, 709),  "opts": [(742, 1289), (1338, 1791), (1840, 2372), (2421, 2978)]}, # graph options
}

def segments(g, roi_top=466, wf_thr=0.55, min_gap=14, min_card=30):
    H, W = g.shape
    wf = (g[:, 8:712] > 248).mean(axis=1)
    iscard = wf >= wf_thr
    s = []; inrun = False; st = 0
    for y in range(roi_top, H):
        if iscard[y] and not inrun: inrun = True; st = y
        elif not iscard[y] and inrun: inrun = False; s.append([st, y-1])
    if inrun: s.append([st, H-1])
    m = []
    for seg in s:
        if m and seg[0]-m[-1][1] < min_gap: m[-1][1] = seg[1]
        else: m.append(seg[:])
    return [tuple(x) for x in m if x[1]-x[0] >= min_card]

def detect(path):
    im = Image.open(path).convert('RGB'); arr = np.array(im).astype(int)
    g = np.array(im.convert('L'))
    R, G, B = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    blue = (B > 130) & (B - R > 45) & (B - G > 25)
    m = segments(g)
    opts = []
    for t, b in m:
        left = blue[t:b, 22:75].sum(); mid = blue[t:b, 300:430].sum()
        if left > 250 and mid < left*0.35:
            opts.append((t, b))
    qsegs = [s for s in m if opts and s[1] < opts[0][0]]
    q = (qsegs[0][0], qsegs[-1][1]) if qsegs else None
    return q, opts

def main(mode="analyze"):
    files = sorted(f for f in os.listdir(SRC) if f.lower().endswith('.jpg'))
    assert len(files) == 58, len(files)
    # capture-order -> (bank_key, prefix, qno)
    plan = []
    for key, prefix, n in BANKS:
        for j in range(n): plan.append((key, prefix))
    assert len(plan) == 58
    per_bank = {}  # key -> {"prefix":.., "questions":[...]}
    per_counter = {}
    flags = []
    for i, f in enumerate(files):
        key, prefix = plan[i]
        per_counter[key] = per_counter.get(key, 0) + 1
        qno = per_counter[key]
        path = os.path.join(SRC, f)
        if i in OVERRIDE:
            q = OVERRIDE[i]["q"]; opts = OVERRIDE[i]["opts"]
        else:
            q, opts = detect(path)
        if q is None or len(opts) not in (3, 4):
            flags.append((i+1, f, len(opts) if opts else 0)); print(f"[FLAG #{i+1}] {f} opts={len(opts) if opts else 0}"); continue
        if len(opts) == 3:
            flags.append((i+1, f, 3))
        if mode == "analyze":
            print(f"#{i+1:2d} {key.split('-')[-1][:6]} q{qno} Q={q} nopts={len(opts)} opts={opts}")
            continue
        im = Image.open(path).convert('RGB'); H = im.size[1]
        # question
        qname = f"{prefix}-q{qno}.jpg"
        im.crop((16, max(0, q[0]-4), 704, min(H, q[1]+6))).save(os.path.join(OUT, qname), quality=90)
        letters = ["a", "b", "c", "d"]; opt_names = {}
        for li, (t, b) in enumerate(opts):
            oname = f"{prefix}-q{qno}-{letters[li]}.jpg"
            im.crop((14, max(0, t-6), 706, min(H, b+6))).save(os.path.join(OUT, oname), quality=90)
            opt_names[letters[li]] = oname
        per_bank.setdefault(key, {"prefix": prefix, "questions": []})
        per_bank[key]["questions"].append({
            "question_no": 2000+qno, "display_no": qno, "year": "KCET",
            "question_image": qname, "option_images": opt_names, "header_in_image": False,
        })
    if mode == "write":
        for key, info in per_bank.items():
            bp = f"/app/backend/chapter_banks/{key}.json"
            with open(bp) as fh: data = json.load(fh)
            found = False
            for sec in data["sections"]:
                if sec["topic"] == "Full Chapter":
                    sec["questions"] = info["questions"]; found = True
            assert found, f"no Full Chapter section in {key}"
            # recompute total across all sections
            data["total_questions"] = sum(len(s["questions"]) for s in data["sections"])
            with open(bp, "w") as fh: json.dump(data, fh, indent=2)
            print(f"WROTE {key}: Full Chapter={len(info['questions'])} total={data['total_questions']}")
    print("FLAGS:", flags)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "analyze")
