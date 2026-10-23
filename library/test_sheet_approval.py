"""Regression tests for individually reviewed supplementary sheets."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SheetApprovalTest(unittest.TestCase):
    def test_only_individually_approved_sheets_are_rendered(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for folder in ('library', 'characters', 'scenes', 'music-videos', 'squad'):
                shutil.copytree(ROOT / folder, root / folder)
            for name in ('README.md', 'CONTENT-NOTICE.md', 'CREDITS.md'):
                shutil.copy2(ROOT / name, root / name)
            path = root / 'library/characters.json'
            manifest = json.loads(path.read_text(encoding='utf-8'))
            teknium = next(c for c in manifest['characters'] if c['id'] == 'teknium')
            for sheet in teknium['sheets']:
                sheet['approval_status'] = 'pending-Mike-review'
            approved = teknium['sheets'][0]
            approved['approval_status'] = 'approved-supplementary'
            approved['label'] = 'Anime alternate'
            path.write_text(json.dumps(manifest), encoding='utf-8')
            subprocess.run([sys.executable, str(root / 'library/build.py')], check=True, capture_output=True)
            reader = (root / 'library/read/characters/sheets/teknium.html').read_text(encoding='utf-8')
            markdown = (root / 'characters/sheets/teknium.md').read_text(encoding='utf-8')
            for text in (reader, markdown):
                self.assertIn(approved['preview'], text)
                for sheet in teknium['sheets'][1:]:
                    self.assertNotIn(sheet['preview'], text)
            approved['approval_status'] = 'pending-Mike-review'
            path.write_text(json.dumps(manifest), encoding='utf-8')
            subprocess.run([sys.executable, str(root / 'library/build.py')], check=True, capture_output=True)
            for relative in ('library/read/characters/sheets/teknium.html', 'characters/sheets/teknium.md', 'characters/teknium.md', 'library/read/characters/teknium.html'):
                text = (root / relative).read_text(encoding='utf-8')
                for sheet in teknium['sheets']:
                    self.assertNotIn(sheet['preview'], text)
                if '/sheets/' in relative:
                    self.assertIn('teknium.', text)
                else:
                    self.assertIn('images/teknium-leafage-shades.png', text)


if __name__ == '__main__':
    unittest.main()
