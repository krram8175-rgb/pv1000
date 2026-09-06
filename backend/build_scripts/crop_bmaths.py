"""Crop Basic Maths (KCET) screenshots -> question + 4 options. Same app layout."""
from PIL import Image
import numpy as np
import os, json, sys

SRC = "/tmp/bm_archive"
OUT = "/app/backend/chapter_images"
BANK = "/app/backend/chapter_banks/neet-math-basic-maths.json"
PREFIX = "bmaths"

PLAN = [
    ("Inequalities", 7),
    ("Logarithm", 1),
    ("Ratio and Proportion", 1),
]

def detect_bands(path, roi_top=295, thr=120, dark_min=4, merge_gap=55, bottom_margin=135):
    a = np.array(Image.open(path).convert('L'))
    H, W = a.shape
    roi_bottom = H - bottom_margin
    darkrows = (a[:, 20:W-20] < thr).sum(axis=1)
    raw = []; inrun = False; s = 0
    for y in range(roi_top, roi_bottom):
        d = darkrows[y] > dark_min
        if d and not inrun: inrun = True; s = y
        elif not d and inrun: inrun = False; raw.append([s, y-1])
    if inrun: raw.append([s, roi_bottom-1])
    merged = []
    for b in raw:
        if merged and b[0]-merged[-1][1] < merge_gap: merged[-1][1] = b[1]
        else: merged.append(b[:])
    return (W, H), [b for b in merged if b[1]-b[0] > 8]

def main(mode="analyze"):
    files = sorted(f for f in os.listdir(SRC) if f.lower().endswith('.jpg'))
    order = []
    for topic, n in PLAN: order += [topic]*n
    assert len(order) == len(files), f"plan {len(order)} vs files {len(files)}"
    sections = {t: [] for t, _ in PLAN}; problems = []
    for i, f in enumerate(files):
        qno = i + 1
        (W, H), bands = detect_bands(os.path.join(SRC, f))
        if len(bands) < 5:
            problems.append((qno, f)); print(f"[FAIL q{qno}] {f} nb={len(bands)} {bands}"); continue
        q = bands[0]; opts = bands[1:5]
        if mode == "analyze":
            print(f"[q{qno}] {order[i][:22]:22s} q={q} opts={opts}"); continue
        im = Image.open(os.path.join(SRC, f)).convert('RGB')
        PAD = 55; x0, x1 = 24, W-24
        qtop = max(295, q[0]-18); qbot = min(H, q[1]+18)
        qname = f"{PREFIX}-q{qno}.jpg"
        im.crop((x0, qtop, x1, qbot)).save(os.path.join(OUT, qname), quality=92)
        letters = ["a", "b", "c", "d"]; opt_names = {}
        for li, (t, b) in enumerate(opts):
            ctop = max(qbot, t-PAD); cbot = min(H, b+PAD)
            oname = f"{PREFIX}-q{qno}-{letters[li]}.jpg"
            im.crop((x0, ctop, x1, cbot)).save(os.path.join(OUT, oname), quality=92)
            opt_names[letters[li]] = oname
        sections[order[i]].append({
            "question_no": qno, "display_no": qno, "year": "KCET 2025",
            "question_image": qname, "option_images": opt_names, "header_in_image": False,
        })
    if mode == "write":
        with open(BANK) as fh: data = json.load(fh)
        total = 0
        for sec in data["sections"]:
            sec["questions"] = sections.get(sec["topic"], []); total += len(sec["questions"])
        data["total_questions"] = total
        with open(BANK, "w") as fh: json.dump(data, fh, indent=2)
        print("WROTE total=", total, {k: len(v) for k, v in sections.items()})
    if problems: print("PROBLEMS:", problems)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "analyze")
