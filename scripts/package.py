#!/usr/bin/env python3
"""Build archives from regular files read through pinned directory handles."""
import hashlib
import os
from pathlib import Path
import stat
import zipfile


def collect(directory, prefix):
    files = []
    for name in sorted(os.listdir(directory)):
        if name in ('.', '..') or '/' in name or '\\' in name:
            raise ValueError('unsafe archive name')
        before = os.stat(name, dir_fd=directory, follow_symlinks=False)
        relative = f'{prefix}/{name}'
        if stat.S_ISDIR(before.st_mode):
            child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory)
            try:
                opened = os.fstat(child)
                if (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino):
                    raise ValueError('directory changed during packaging')
                files.extend(collect(child, relative))
            finally:
                os.close(child)
        elif stat.S_ISREG(before.st_mode):
            fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
            try:
                opened = os.fstat(fd)
                if not stat.S_ISREG(opened.st_mode) or (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino):
                    raise ValueError('file changed during packaging')
                with os.fdopen(fd, 'rb', closefd=False) as stream:
                    content = stream.read()
                after = os.fstat(fd)
                if (opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns) != (after.st_size, after.st_mtime_ns, after.st_ctime_ns):
                    raise ValueError('file changed during packaging')
                files.append((relative, content))
            finally:
                os.close(fd)
        else:
            raise ValueError('symlinks and special files are not package inputs')
    return files


def package(skills, output):
    fd = os.open(skills, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        # Validate and snapshot every input before creating any archive.
        snapshots = []
        for name in sorted(os.listdir(fd)):
            child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            try:
                snapshots.append((name, collect(child, name)))
            finally:
                os.close(child)
    finally:
        os.close(fd)
    output.mkdir(parents=True, exist_ok=True)
    sums = []
    for name, files in snapshots:
        target = output / f'{name}.zip'
        with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            for relative, content in files:
                info = zipfile.ZipInfo(relative, date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = (stat.S_IFREG | 0o644) << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, content)
        with zipfile.ZipFile(target) as archive:
            expected = {relative for relative, _ in files}
            if set(archive.namelist()) != expected or archive.testzip() is not None:
                raise ValueError('archive verification failed')
            for info in archive.infolist():
                if not stat.S_ISREG(info.external_attr >> 16) or not info.filename.startswith(name + '/'):
                    raise ValueError('unsafe archive member')
        sums.append(f'{hashlib.sha256(target.read_bytes()).hexdigest()}  {target.name}\n')
    (output / 'SHA256SUMS').write_text(''.join(sums))


if __name__ == '__main__':
    root = Path(__file__).resolve().parent.parent
    package(root / 'skills', root / 'dist')
