"""Match idle scale and yellow tone to the existing jump landing reference."""
from pathlib import Path
import argparse
import colorsys
import json
from statistics import median
from PIL import Image


def normalize(path):
    atlas = Image.open(path).convert('RGBA')
    idle = atlas.crop((0, 0, 192, 208))
    landing = atlas.crop((768, 832, 960, 1040))

    def bounds(im):
        return im.getchannel('A').point(lambda x: 255 if x > 100 else 0).getbbox()

    def belly_color(im):
        x0, y0, x1, y1 = bounds(im)
        region = im.crop((round(x0+(x1-x0)*.36), round(y0+(y1-y0)*.57),
                          round(x0+(x1-x0)*.64), round(y0+(y1-y0)*.78)))
        pixels = [p for p in region.getdata() if p[3] > 250]
        return [median(p[i] for p in pixels) for i in range(3)]

    source_box, target_box = bounds(idle), bounds(landing)
    scale = (target_box[3]-target_box[1])/(source_box[3]-source_box[1])
    source_color, target_color = belly_color(idle), belly_color(landing)
    delta = [t-s for s, t in zip(source_color, target_color)]
    # Same transform for all six idle frames plus the dedicated neutral cell.
    # A shared foot anchor retains the original breathing/blinking displacement.
    for col in range(7):
        cell = atlas.crop((col*192, 0, (col+1)*192, 208))
        pixels = []
        for red, green, blue, alpha in cell.getdata():
            if not alpha:
                pixels.append((0, 0, 0, 0))
                continue
            hue, saturation, value = colorsys.rgb_to_hsv(red/255, green/255, blue/255)
            weight = min(1, max(0, (value-.55)/.2)) * min(1, saturation/.3)
            if not .07 < hue < .22:
                weight = 0
            rgb = [round(min(255, max(0, v + shift*weight)))
                   for v, shift in zip((red, green, blue), delta)]
            pixels.append((*rgb, alpha))
        cell.putdata(pixels)
        width, height = round(192*scale), round(208*scale)
        scaled = cell.resize((width, height), Image.Resampling.LANCZOS)
        result = Image.new('RGBA', (192, 208))
        top = round(target_box[3] - source_box[3]*(height/208))
        result.alpha_composite(scaled, ((192-width)//2, top))
        result.putdata([p if p[3] else (0, 0, 0, 0) for p in result.getdata()])
        atlas.paste(result, (col*192, 0))
    atlas.save(path, lossless=True, exact=True)
    return {'scale': scale, 'source_belly_rgb': source_color,
            'target_belly_rgb': target_color, 'channel_offset': delta,
            'changed_cells': ['r0c'+str(i) for i in range(7)]}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('atlas', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = normalize(args.atlas)
    if args.report:
        args.report.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))
