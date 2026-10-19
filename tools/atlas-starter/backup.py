"""Back up the atlas source before every change.

    uv run backup.py            -> out/backups/<YYYYmmdd-HHMMSS>.tar.gz

Run it before you, or an agent, edit the kit, a part or a map. On the worked example, untracked
mockups and specs were overwritten in place by an agent and had no backup; they were rebuilt from
transcripts. Untracked files have no git history to fall back on.
"""
import datetime
import pathlib
import tarfile

HERE = pathlib.Path(__file__).parent
SOURCES = ['kit.py', 'parts', 'spec_map.py', 'backend_map.py']

if __name__ == '__main__':
    dest = HERE / 'out' / 'backups'
    dest.mkdir(parents=True, exist_ok=True)
    path = dest / f'{datetime.datetime.now():%Y%m%d-%H%M%S}.tar.gz'
    with tarfile.open(path, 'w:gz') as tar:
        for s in SOURCES:
            tar.add(HERE / s, arcname=s, filter=lambda t: None if '__pycache__' in t.name else t)
    print(path)
