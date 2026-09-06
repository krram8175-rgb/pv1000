"""Crop Matrices question screenshots into question + 4 option images.
Source: user-provided app screenshots (fixed layout, 720px wide, variable height).
"""
from PIL import Image
import numpy as np
import os, json, sys

SRC = "/tmp/mat_archive"
OUT = "/app/backend/chapter_images"
BANK = "/app/backend/chapter_banks/neet-math-matrices.json"

# capture-order -> topic mapping (counts from user)
PLAN = [
    ("Product of Matrices", 11),
    ("Inverse of a Matrix", 8),
    ("Adjoint and its Properties", 5),
    ("Basic Algebra of Matrices", 6),
    ("Symmetric & Skew Symmetric Matrices", 6),
    ("System of Linear Equations", 1),
    ("Formation and Basic of Matrix", 1),
]

def detect_bands(path, roi_top=295, thr=120, dark_min=8, merge_gap=55, bottom_margin=135):
    im = Image.open(path).convert('L')
    a = np.array(im)
    H, W = a.shape
    roi_bottom = H - bottom_margin
    sub = a[:, 20:W-20]
    darkrows = (sub < thr).sum(axis=1)
    raw = []
    inrun = False; s = 0
    for y in range(roi_top, roi_bottom):
        d = darkrows[y] > dark_min
        if d and not inrun:
            inrun = True; s = y
        elif not d and inrun:
            inrun = False; raw.append([s, y-1])
    if inrun:
        raw.append([s, roi_bottom-1])
    merged = []
    for b in raw:
        if merged and b[0]-merged[-1][1] < merge_gap:
            merged[-1][1] = b[1]
        else:
            merged.append(b[:])
    merged = [b for b in merged if b[1]-b[0] > 8]
    return (W, H), merged

def main(mode="analyze"):
    files = sorted(f for f in os.listdir(SRC) if f.lower().endswith('.jpg'))
    assert len(files) == 38, f"expected 38, got {len(files)}"
    # build capture-order -> topic list
    order = []
    for topic, n in PLAN:
        order += [topic]*n
    assert len(order) == 38

    sections = {topic: [] for topic, _ in PLAN}
    problems = []
    for i, f in enumerate(files):
        qno = i + 1
        (W, H), bands = detect_bands(os.path.join(SRC, f))
        ok = len(bands) >= 5
        if not ok:
            problems.append((qno, f, len(bands), bands))
            print(f"[FAIL q{qno}] {f} nbands={len(bands)} {bands}")
            continue
        q = bands[0]
        opts = bands[1:5]
        if mode == "analyze":
            print(f"[q{qno}] {order[i]:32s} nb={len(bands)} q={q} opts={[o for o in opts]}")
            continue
        # crop and save
        im = Image.open(os.path.join(SRC, f)).convert('RGB')
        PAD = 55
        x0, x1 = 24, W-24
        # question
        qtop = max(295, q[0]-18); qbot = min(H, q[1]+18)
        qimg = im.crop((x0, qtop, x1, qbot))
        qname = f"mat-q{qno}.jpg"
        qimg.save(os.path.join(OUT, qname), quality=92)
        letters = ["a", "b", "c", "d"]
        opt_names = {}
        for li, (t, b) in enumerate(opts):
            ctop = max(qbot, t-PAD); cbot = min(H, b+PAD)
            oimg = im.crop((x0, ctop, x1, cbot))
            oname = f"mat-q{qno}-{letters[li]}.jpg"
            oimg.save(os.path.join(OUT, oname), quality=92)
            opt_names[letters[li]] = oname
        sections[order[i]].append({
            "question_no": qno,
            "display_no": qno,
            "year": "KCET 2025",
            "question_image": qname,
            "option_images": opt_names,
            "header_in_image": False,
        })
    if mode == "write":
        # load bank, populate sections in existing section order
        with open(BANK) as fh:
            data = json.load(fh)
        total = 0
        for sec in data["sections"]:
            qs = sections.get(sec["topic"], [])
            sec["questions"] = qs
            total += len(qs)
        data["total_questions"] = total
        with open(BANK, "w") as fh:
            json.dump(data, fh, indent=2)
        print(f"WROTE bank total_questions={total}")
        print("per-topic:", {k: len(v) for k, v in sections.items()})
    if problems:
        print("PROBLEMS:", problems)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "analyze")
