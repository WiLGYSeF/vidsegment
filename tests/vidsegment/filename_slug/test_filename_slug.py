from re import M
import unittest

from src.vidsegment.filename_slug import FilenameSlug

class FilenameSlugTests(unittest.TestCase):
    def test_slug_filename_linux(self):
        slugr = FilenameSlug('linux')

        entries = {
            '': '',
            '/test/asdf': '\u2215test\u2215asdf',
            'abcdef': 'abcdef',
            '.': '\u00b7',
        }

        for filename, expected in entries.items():
            self.assertEqual(expected, slugr.slug_filename(filename))

    def test_slug_filename_windows(self):
        slugr = FilenameSlug('windows')

        entries = {
            '': '',
            r'C:\test\asdf': 'C\uff1a\uff3ctest\uff3casdf',
            r'abc\123': 'abc\uff3c123',
            'abcdef': 'abcdef',
            'w/hat?': 'w\u2215hat\uff1f',
            'CON': 'CON_',
            '.': '\u00b7',
        }

        for filename, expected in entries.items():
            self.assertEqual(expected, slugr.slug_filename(filename))

    def test_slug_filename_unknown(self):
        slugr = FilenameSlug('unknown')

        with self.assertRaises(ValueError):
            slugr.slug_filename('abcdef')
