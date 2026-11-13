"""Build/check the source-only directory submission from canonical skill files."""
import argparse
import os
import struct
from pathlib import Path
import stat

from package import collect

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / 'plugin'


def snapshot(directory, prefix):
    fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        return dict(collect(fd, prefix))
    finally:
        os.close(fd)


def expected_files():
    files = snapshot(ROOT / 'skills', 'skills')
    files.update(snapshot(ROOT / '.claude-plugin', '.claude-plugin'))
    # The submission is a plugin, not the development repository's marketplace.
    files.pop('.claude-plugin/marketplace.json')
    # The directory discovers this default filename without a manifest icon field.
    icon = files['.claude-plugin/icon.png']
    if icon[:8] != b'\x89PNG\r\n\x1a\n' or len(icon) >= 2 * 1024 * 1024:
        raise ValueError('Icon must be a PNG under 2 MB')
    width, height = struct.unpack('>II', icon[16:24])
    if width != height or not 512 <= width <= 2048:
        raise ValueError('Icon must be square, 512–2048 pixels')
    files['LICENSE.txt'] = (ROOT / 'LICENSE').read_bytes()
    files['README.md'] = (ROOT / 'PLUGIN_README.md').read_bytes()
    for name, content in files.items():
        if Path(name).suffix not in {'.md', '.txt', '.json', '.png'}:
            raise ValueError(f'Unsupported submission file: {name}')
        if not name.endswith('.png'):
            content.decode('utf-8')
            if b'\0' in content:
                raise ValueError(f'NUL in submission text: {name}')
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    expected = expected_files()
    actual = snapshot(DEST, '') if DEST.exists() else {}
    actual = {name.lstrip('/'): data for name, data in actual.items()}
    if args.check:
        if actual != expected:
            raise SystemExit('Submission differs from source; run python3 scripts/build_plugin.py')
    else:
        # Refuse links/special files via snapshot before modifying the generated tree.
        for name in actual.keys() - expected.keys():
            (DEST / name).unlink()
        for name, content in expected.items():
            target = DEST / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
            target.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    print(f'{len(expected)} submission files match canonical source' if args.check else f'Built {len(expected)} submission files in plugin/')


if __name__ == '__main__':
    main()
