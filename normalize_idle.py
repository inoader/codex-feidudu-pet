"""Match idle and hover using existing landing artwork and aligned eyelid art.

Input: freshly assembled unnormalized atlas, never an already processed atlas.
"""
from pathlib import Path
import argparse
import json
from statistics import median
from PIL import Image


def eye_boxes(im):
    p = im.load()
    remaining = {(x, y) for y in range(42, 90) for x in range(55, 120)
                 if p[x, y][0] > 170 and p[x, y][1] > 150
                 and p[x, y][2] > 110 and p[x, y][3] > 240}
    groups = []
    while remaining:
        stack, group = [remaining.pop()], []
        while stack:
            x, y = stack.pop()
            group.append((x, y))
            for point in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
                if point in remaining:
                    remaining.remove(point)
                    stack.append(point)
        if len(group) > 7:
            xs, ys = zip(*group)
            groups.append((min(xs), min(ys), max(xs)+1, max(ys)+1))
    if len(groups) != 2:
        raise ValueError(f'Expected two eye whites, found {groups}')
    return sorted(groups)


def normalize(path):
    atlas = Image.open(path).convert('RGBA')
    open_eye = atlas.crop((0, 0, 192, 208))
    half_eye = atlas.crop((384, 0, 576, 208))
    landing = atlas.crop((768, 832, 960, 1040))
    blink, boxes = landing.copy(), []
    for source, target in zip(eye_boxes(open_eye), eye_boxes(landing)):
        pad = 3
        sb = (source[0]-pad, source[1]-pad, source[2]+pad, source[3]+pad)
        tb = (target[0]-pad, target[1]-pad, target[2]+pad, target[3]+pad)
        size = (tb[2]-tb[0], tb[3]-tb[1])
        donor = half_eye.crop(sb).resize(size, Image.Resampling.LANCZOS)
        backdrop = landing.crop(tb)
        dp, bp = donor.load(), backdrop.load()
        w, h = size
        rim = [(x, y) for y in range(h) for x in range(w)
               if min(x, y, w-1-x, h-1-y) < 2]
        offset = [median(bp[x, y][c]-dp[x, y][c] for x, y in rim) for c in range(3)]
        for y in range(h):
            for x in range(w):
                weight = min(1., min(x, y, w-1-x, h-1-y)/3.)
                rgb = tuple(round(bp[x, y][c]*(1-weight) +
                                  max(0, min(255, dp[x, y][c]+offset[c]))*weight)
                            for c in range(3))
                blink.putpixel((tb[0]+x, tb[1]+y), (*rgb, bp[x, y][3]))
        boxes.append(tb)
    # Runtime stretches idle6x: one short, shallow eyelid gesture avoids a
    # 1500ms half/fully shut hold. Neutral and every open frame match landing.
    for col in range(7):
        atlas.paste(blink if col == 1 else landing, (col*192, 0))
    # Preserve jump foot travel with the identical character artwork.
    offsets = [0, 2, -9, 1, 0]
    for col, dy in enumerate(offsets):
        frame = Image.new('RGBA', (192, 208))
        frame.paste(landing, (0, dy))
        atlas.paste(frame, (col*192, 832))
    atlas.putdata([p if p[3] else (0, 0, 0, 0) for p in atlas.getdata()])
    atlas.save(path, lossless=True, exact=True)
    return {'canonical': 'jumping frame4', 'idle_durations_ms': [1680,660,660,840,840,1920],
            'eyelid_frame': 1, 'eyelid_hold_ms': 660, 'fully_closed_hold_ms': 0,
            'eye_patch_boxes': boxes, 'jump_y_offsets': offsets,
            'changed_rows': [0,4], 'color_strategy': 'shared exact artwork, no per-state tint'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('atlas', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = normalize(args.atlas)
    if args.report:
        args.report.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))
