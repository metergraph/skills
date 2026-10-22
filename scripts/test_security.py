"""Synthetic publication and archive boundary regressions; no external services."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('skill_package', ROOT / 'scripts/package.py')
pack = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pack)


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        self.git('init', '-q', '-b', 'main')
        self.git('config', 'user.email', 'test@example.com')
        self.git('config', 'user.name', 'Synthetic Test')
        self.commit('base')
        self.git('branch', 'baseline')

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.repo, text=True)

    def commit(self, message):
        self.git('add', '.')
        self.git('commit', '-q', '--allow-empty', '-m', message)

    def check(self, event=None):
        env = dict(os.environ)
        env.pop('GITHUB_EVENT_PATH', None)
        if event:
            file = self.repo / '.event.json'
            file.write_text(json.dumps(event))
            env['GITHUB_EVENT_PATH'] = str(file)
        return subprocess.run(['python3', str(ROOT / 'scripts/check_publication.py'), 'baseline'], cwd=self.repo, env=env, capture_output=True, text=True).returncode

    def test_clean_control(self):
        (self.repo / 'example.txt').write_text('ordinary text\n')
        self.commit('ordinary change')
        self.assertEqual(self.check(), 0)

    def test_local_and_pr_branch(self):
        private = 'topic/' + 'MET' + '-123'
        self.git('checkout', '-q', '-b', private)
        self.assertEqual(self.check(), 1)
        self.git('checkout', '-q', 'main')
        self.assertEqual(self.check({'pull_request': {'head': {'ref': private}}}), 1)

    def test_added_plus_prefix_and_removed_intermediate(self):
        (self.repo / 'example.txt').write_text('++' + 'MET' + '-123\n')
        self.commit('introduce text')
        self.assertEqual(self.check(), 1)
        (self.repo / 'example.txt').write_text('ordinary text\n')
        self.commit('remove text')
        self.assertEqual(self.check(), 1)

    def test_private_filename(self):
        (self.repo / ('MET' + '-123.txt')).write_text('ordinary text\n')
        self.commit('add file')
        self.assertEqual(self.check(), 1)

    def test_binary_attribute_cannot_hide_content(self):
        (self.repo / '.gitattributes').write_text('payload.txt -diff\n')
        (self.repo / 'payload.txt').write_bytes(b'binary\0' + b'MET' + b'-123\n')
        self.commit('add data')
        self.assertEqual(self.check(), 1)



class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.skills = self.root / 'skills'
        self.skill = self.skills / 'metergraph-example'
        self.skill.mkdir(parents=True)
        (self.skill / 'SKILL.md').write_text('synthetic regular content\n')
        self.output = self.root / 'out'

    def test_regular_files_preserved(self):
        (self.skill / 'references').mkdir()
        (self.skill / 'references/example.md').write_text('nested content\n')
        pack.package(self.skills, self.output)
        with zipfile.ZipFile(self.output / 'metergraph-example.zip') as archive:
            self.assertEqual(archive.read('metergraph-example/references/example.md'), b'nested content\n')
            self.assertEqual(len(archive.namelist()), 2)

    def test_nested_absolute_and_relative_links_rejected_before_output(self):
        outside = self.root / 'outside.txt'
        outside.write_text('never archive this\n')
        nested = self.skill / 'references'
        nested.mkdir()
        link = nested / 'leak'
        for target in [outside, Path('../../../outside.txt')]:
            link.symlink_to(target)
            with self.assertRaises((OSError, ValueError)):
                pack.package(self.skills, self.output)
            self.assertFalse(self.output.exists())
            link.unlink()

    def test_special_file_rejected(self):
        os.mkfifo(self.skill / 'pipe')
        with self.assertRaises((OSError, ValueError)):
            pack.package(self.skills, self.output)
        self.assertFalse(self.output.exists())

    def test_validator_rejects_nested_link(self):
        target = self.root / 'repo'
        shutil.copytree(ROOT / 'scripts', target / 'scripts', ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copytree(ROOT / 'skills', target / 'skills')
        shutil.copytree(ROOT / '.claude-plugin', target / '.claude-plugin')
        nested = target / 'skills/metergraph/references'
        nested.mkdir(exist_ok=True)
        (nested / 'leak').symlink_to(ROOT / 'README.md')
        result = subprocess.run(['node', 'scripts/validate.mjs'], cwd=target, capture_output=True)
        self.assertNotEqual(result.returncode, 0)


if __name__ == '__main__':
    unittest.main()
