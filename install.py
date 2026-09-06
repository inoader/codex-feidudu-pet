"""Install the bundled pet using only the Python standard library."""
import argparse
import json
import os
from pathlib import Path
import shutil

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--replace', action='store_true', help='Replace an existing installation')
args = parser.parse_args()
source = Path(__file__).resolve().parent
home = Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex').expanduser()
target = home / 'pets' / 'meituan-feidudu'
if target.exists() and not args.replace:
    parser.error(f'{target} already exists; use --replace to overwrite')
manifest = json.loads((source / 'pet.json').read_text(encoding='utf-8'))
assert manifest['spritesheetPath'] == 'spritesheet.png'
assert (source / 'spritesheet.png').is_file()
target.mkdir(parents=True, exist_ok=True)
for name in ('pet.json', 'spritesheet.png'):
    shutil.copy2(source / name, target / name)
print(f'Installed: {target}')
print('Reopen Codex and select 肥嘟嘟 · 美团袋鼠 in the pet picker.')
