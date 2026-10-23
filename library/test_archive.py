"""Content and static-reader regression checks (run after build.py)."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ArchiveTest(unittest.TestCase):
    def test_collaborative_credits_have_a_readable_front_door(self):
        home = (ROOT / 'library/index.html').read_text(encoding='utf-8')
        self.assertIn('Collaborative character bible', home)
        self.assertIn('read/CREDITS.html', home)
        credits = (ROOT / 'CREDITS.md').read_text(encoding='utf-8')
        for name in ('123mikeyd', 'ArtsBro', 'Sahil', 'Quark2world'):
            self.assertIn(name, credits)
        for slug in ('doge-man', 'artsbro', 'sahil', 'quark2world'):
            text = (ROOT / f'characters/{slug}.md').read_text(encoding='utf-8')
            self.assertIn('NRCU co-artist', text)
            self.assertIn('../CREDITS.md', text)
        self.assertTrue((ROOT / 'library/read/CREDITS.html').exists())

    def test_selected_references_and_shared_identity_are_preserved(self):
        entries = json.loads((ROOT / 'library/characters.json').read_text())['characters']
        cast = {c['id']: c for c in entries}
        for slug, image in {'artsbro':'artsbro-masked-full-body.png','ee-dd':'ee-dd-landscape.png','teknium':'teknium-leafage-shades.png','nous-girl':'nous-girl-reference.png','noctis':'noctis-sheet.png'}.items():
            self.assertEqual(cast[slug]['primary_reference'], 'images/' + image)
        self.assertEqual(cast['gille']['profile'], cast['coffeeblender']['profile'])
        self.assertNotIn('123mikeyd', cast)
        self.assertIn('Super Shiba', cast['doge-man']['aliases'])
        self.assertEqual({c['group'] for c in entries}, {'nous'})
        self.assertNotIn('bobo', cast)
        self.assertNotIn('ice-mage', cast)

    def test_teknium_approved_set_matches_current_profile(self):
        cast = json.loads((ROOT / 'library/characters.json').read_text())['characters']
        tek = next(c for c in cast if c['id'] == 'teknium')
        expected = {'anime','chess-themed-pose-expression','chibi','disney','gothic','ink-pen-sketch','mecha','punk','rick-and-morty'}
        self.assertEqual({s['style'] for s in tek['sheets'] if s.get('approval_status') == 'approved-supplementary'}, expected)
        for path in ('characters/teknium.md', 'characters/sheets/teknium.md', 'library/read/characters/teknium.html', 'library/read/characters/sheets/teknium.html'):
            text = (ROOT / path).read_text(encoding='utf-8')
            for sheet in tek['sheets']:
                if sheet['style'] in expected:
                    self.assertIn(sheet['preview'], text)
                else:
                    self.assertNotIn(sheet['preview'], text)

if __name__ == '__main__':
    unittest.main()
