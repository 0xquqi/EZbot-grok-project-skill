"""Exercise packaging integrity and rejection paths in isolated temporary copies."""
import hashlib
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='ezbot-release-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for directory in ('skills', 'evaluation', 'tools'):
            shutil.copytree(ROOT / directory, self.root / directory)
        for filename in ('开始使用.txt', '给现有Grok对话的纠正指令.txt', 'LICENSE'):
            shutil.copy2(ROOT / filename, self.root / filename)
        self.run_build()

    def run_build(self, *args, success=True, optimize=False):
        command = [sys.executable] + (['-O'] if optimize else [])
        result = subprocess.run(command + ['tools/build_release.py', *args],
                                cwd=self.root, capture_output=True, text=True)
        if success:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout)
        return result

    def test_rebuild_is_identical_and_excludes_runtime_files(self):
        archive = self.root / 'EZbot-Grok-Scout-v0.1.zip'
        before = hashlib.sha256(archive.read_bytes()).hexdigest()
        (self.root / 'state.json').write_text('{"private_fixture":true}')
        (self.root / 'old-release.zip').write_bytes(b'not for delivery')
        self.run_build()
        self.run_build('--check')
        self.assertEqual(before, hashlib.sha256(archive.read_bytes()).hexdigest())
        with zipfile.ZipFile(archive) as package:
            names = package.namelist()
            self.assertTrue(any(name.endswith('/LICENSE') for name in names))
            self.assertFalse(any(name.endswith('/state.json') or name.endswith('/old-release.zip') for name in names))

    def test_stale_source_is_rejected(self):
        path = self.root / 'skills/ezbot-grok-scout/references/research-flow.md'
        path.write_text(path.read_text() + '\nNew research rule.\n')
        result = self.run_build('--check', success=False)
        self.assertIn('Stale delivery file', result.stderr)

    def test_modified_archive_is_rejected(self):
        archive = self.root / 'EZbot-Grok-Scout-v0.1.zip'
        with zipfile.ZipFile(archive, 'a') as package:
            package.writestr('unexpected.txt', 'not part of release')
        self.run_build('--check', success=False)

    def test_broken_reference_is_rejected(self):
        path = self.root / 'skills/ezbot-grok-scout/references/output.md'
        path.write_text(path.read_text() + '\n[Missing](missing.md)\n')
        self.run_build(success=False)

    def test_personal_path_is_rejected(self):
        path = self.root / '开始使用.txt'
        path.write_text(path.read_text() + '\n/Users/example/private-state.json\n')
        self.run_build(success=False)

    def test_optimized_python_cannot_skip_validation(self):
        result = self.run_build('--check', success=False, optimize=True)
        self.assertIn('validation assertions must remain enabled', result.stderr)


if __name__ == '__main__':
    unittest.main()
