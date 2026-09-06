"""Crop 'Explanation' sections and wire as solution_image for a chapter bank section.
Usage: python3 crop_chapter.py <src_dir> <bank_json> <section_index> <img_prefix>
Screenshots matched in sorted order to that section's questions in order.
"""
import glob, os, sys, json
from PIL import Image
from crop_explanations import detect

IMG_DIR = "/app/backend/chapter_images"


def main():
    src, bank_path, sec_idx, prefix = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
    files = sorted(glob.glob(os.path.join(src, 'Screenshot_*.jpg')))
    data = json.load(open(bank_path))
    qs = data['sections'][sec_idx]['questions']
    n = min(len(files), len(qs))
    done = 0
    for i in range(n):
        box = detect(Image.open(files[i]))
        qno = qs[i]['question_no']
        if not box:
            print('WARN no header:', qno, os.path.basename(files[i])); continue
        name = f'{prefix}-q{qno}-sol.png'
        Image.open(files[i]).crop(box).save(os.path.join(IMG_DIR, name))
        qs[i]['solution_image'] = name
        done += 1
        print(qno, os.path.basename(files[i]), 'h=', box[3] - box[1])
    json.dump(data, open(bank_path, 'w'), ensure_ascii=False, indent=2)
    print('WROTE solution_image for', done, 'questions (files=%d, section_q=%d)' % (len(files), len(qs)))


if __name__ == '__main__':
    main()
