import sys, os
import numpy as np
from PIL import Image
sys.path.insert(0, '/app/backend/build_scripts')
from crop_explanations import detect

IMG_DIR = '/app/backend/chapter_images'
OUT = '/tmp/art6/out'
os.makedirs(OUT, exist_ok=True)

Q8 = '/tmp/art6/Screenshot_2026-09-05-21-52-06-27_40deb401b9ffe8e1df2f1cc5ba480b12.jpg'  # balloon options
Q5 = '/tmp/art6/Screenshot_2026-09-05-21-52-21-03_40deb401b9ffe8e1df2f1cc5ba480b12.jpg'  # vernier explanation


def trim(im2, pad=10):
    g = np.array(im2.convert('L'))
    ys, xs = np.where(g < 235)
    if len(ys) == 0:
        return im2
    return im2.crop((max(0, xs.min() - pad), max(0, ys.min() - pad),
                     min(im2.width, xs.max() + pad), min(im2.height, ys.max() + pad)))


def find_gaps(a, y_from, y_to, x0=20, x1=680):
    strip = a[:, x0:x1, :]
    mn = strip.min(axis=2); mx = strip.max(axis=2)
    graylike = (strip[:, :, 0] >= 234) & (strip[:, :, 0] <= 247) & (mx - mn < 12)
    white = strip.min(axis=2) >= 249
    dark = strip.max(axis=2) < 205
    fg, fw, fd = graylike.mean(axis=1), white.mean(axis=1), dark.mean(axis=1)
    gap = (fg > 0.80) & (fw < 0.05) & (fd < 0.02)
    ys = [y for y in range(y_from, y_to) if gap[y]]
    bands = []
    if ys:
        s = prev = ys[0]
        for y in ys[1:]:
            if y - prev > 6:
                bands.append((s, prev)); s = y
            prev = y
        bands.append((s, prev))
    return bands


# ---------- Q8 options (balloon) ----------
im8 = Image.open(Q8).convert('RGB'); a8 = np.array(im8).astype(int)
ebox8 = detect(im8)  # explanation header not present here -> may be None; use bottom fallback
top_lim = ebox8[1] if ebox8 else a8.shape[0]
gaps = find_gaps(a8, 255, min(top_lim, a8.shape[0]) - 2)
print('Q8 gap mids:', [(g[0]+g[1])//2 for g in gaps])
# cards sit between consecutive gaps
cards = []
for i in range(len(gaps) - 1):
    cards.append((gaps[i][1] + 1, gaps[i + 1][0] - 1))
# keep 4 largest (option cards)
cards = sorted(cards, key=lambda c: c[1] - c[0], reverse=True)[:4]
cards = sorted(cards)
print('Q8 cards:', cards)
OX0, OX1 = 12, 655
for L, (y0, y1) in zip('abcd', cards):
    crop = im8.crop((OX0, y0, OX1, y1))
    crop = trim(crop, pad=10)
    crop.save(f'{OUT}/q8-{L}.png')
    print('q8', L, crop.size)

# ---------- Q5 explanation (vernier) ----------
im5 = Image.open(Q5).convert('RGB')
b5 = detect(im5)
ex = trim(im5.crop((b5[0], b5[1], b5[2], b5[3])), pad=12)
ex.save(f'{OUT}/q5-sol.png')
print('q5 sol', ex.size)
