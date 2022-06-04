import unittest

from src.vidsegment.utils.time_to_seconds import time_to_seconds

class TimeToSecondsTests(unittest.TestCase):
    def test_time_to_seconds(self):
        entries = {
            'a': None,
            '123': None,
            '61': None,
            '1': 1,
            '23': 23,
            '1:00': 60,
            '1:23': 60 + 23,
            '19:27': 19 * 60 + 27,
            '2:05:22': 2 * 3600 + 5 * 60 + 22,
            '1:2:3': 1 * 3600 + 2 * 60 + 3,
        }

        for key, val in entries.items():
            with self.subTest(time=key):
                if val is not None:
                    self.assertEqual(val, time_to_seconds(key))
                else:
                    with self.assertRaises(ValueError):
                        time_to_seconds(key)
