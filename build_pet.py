"""Rebuild the v2 atlas from approved rows using an installed hatch-pet skill."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--skill-dir', type=Path, default=Path.home()/'.codex/skills/hatch-pet')
args = parser.parse_args()
root = Path(__file__).resolve().parent
scripts = args.skill_dir / 'scripts'
if not (scripts / 'assemble_extended_atlas.py').is_file():
    parser.error('Install hatch-pet or pass --skill-dir pointing to its directory')
work = root / '.build-pet'
decoded = work / 'decoded'
frames = work / 'frames'
final = work / 'final'
qa = work / 'qa'
for path in (decoded, frames, final, qa):
    path.mkdir(parents=True, exist_ok=True)
for source in (root / 'source' / 'rows').glob('*.png'):
    shutil.copy2(source, decoded / source.name)

def run(script, *arguments):
    subprocess.run([sys.executable, str(scripts/script), *map(str, arguments)], check=True)

run('extract_strip_frames.py', '--decoded-dir', decoded, '--output-dir', frames,
    '--states', 'all', '--method', 'stable-slots', '--chroma-key', '#0000FF')
run('inspect_frames.py', '--frames-root', frames, '--json-out', qa/'review.json',
    '--require-components', '--allow-stable-slots')
run('compose_atlas.py', '--frames-root', frames, '--output', final/'standard.png',
    '--webp-output', final/'standard.webp')
run('assemble_extended_atlas.py', '--base-atlas', final/'standard.webp',
    '--look-row-9', decoded/'look-row-9.png', '--neutral-cell', frames/'idle/00.png',
    '--chroma-key', '#0000FF', '--chroma-threshold', '96',
    '--registered-row-output', qa/'row9.png',
    '--registration-manifest-output', qa/'registration.json')
run('assemble_extended_atlas.py', '--base-atlas', final/'standard.webp',
    '--registered-row-9', qa/'row9.png', '--row-9-registration', qa/'registration.json',
    '--look-row-10', decoded/'look-row-10.png', '--neutral-cell', frames/'idle/00.png',
    '--chroma-key', '#0000FF', '--chroma-threshold', '96',
    '--output', final/'extended.png', '--webp-output', final/'extended.webp',
    '--manifest-output', final/'atlas.json')
run('despill_chroma_edges.py', final/'extended.png', '--output', final/'extended.png',
    '--webp-output', final/'extended.webp', '--chroma-key', '#0000FF',
    '--json-out', qa/'despill.json')
run('validate_atlas.py', final/'extended.webp', '--require-v2', '--chroma-key', '#0000FF',
    '--json-out', qa/'validation.json')
shutil.copy2(final/'extended.webp', root/'spritesheet.webp')
subprocess.run([sys.executable, str(root/'normalize_idle.py'), str(root/'spritesheet.webp')], check=True)
run('validate_atlas.py', root/'spritesheet.webp', '--require-v2', '--chroma-key', '#0000FF',
    '--json-out', qa/'validation-normalized.json')
print('Rebuilt spritesheet.webp; inspect visual QA before installing modified rows.')
