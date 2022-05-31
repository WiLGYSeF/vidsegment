import unittest

from src.vidsegment.utils.seconds_to_time import seconds_to_time

class SecondsToTimeTests(unittest.TestCase):
    def test_seconds_to_time(self):
        entries = {
            1: '00:01',
            23: '00:23',
            60: '01:00',
            47.23: '00:47.23',
            12.0: '00:12',
            60 + 23: '01:23',
            19 * 60 + 27: '19:27',
            2 * 3600 + 5 * 60 + 22: '02:05:22',
            1 * 3600 + 2 * 60 + 3: '01:02:03',
        }

        for key, val in entries.items():
            with self.subTest(seconds=key):
                if val is not None:
                    self.assertEqual(val, seconds_to_time(key))
                else:
                    with self.assertRaises(ValueError):
                        seconds_to_time(key)
