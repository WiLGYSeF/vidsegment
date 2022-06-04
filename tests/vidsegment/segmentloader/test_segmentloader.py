import unittest
from unittest.mock import mock_open, patch

from src.vidsegment.segmentloader import SegmentLoader

class SegmentLoaderTests(unittest.TestCase):
    def test_load_yaml(self):
        entries = [
            (
"""
segments:
  - start: 12
    end: 24
    filename: abcdef
    title: asdf
    volume: 1.5
    constant_rate_factor: 20
    metadata:
      comment: aaaaaa
""",
                [
                    {
                        'start': 12,
                        'end': 24,
                        'filename': 'abcdef',
                        'title': 'asdf',
                        'volume': '1.5',
                        'constant_rate_factor': 20,
                        'metadata': {
                            'comment': 'aaaaaa'
                        },
                    },
                ]
            ),
            (
"""
filename: test
segments:
  - start: 0
    end: 15
  - start: '1:23'
    end: '02:21'
""",
                [
                    {
                        'start': 0,
                        'end': 15,
                        'filename': 'test',
                        'title': None,
                        'volume': None,
                        'metadata': None,
                    },
                    {
                        'start': 60 + 23,
                        'end': 2 * 60 + 21,
                        'filename': 'test',
                        'title': None,
                        'volume': None,
                        'metadata': None,
                    },
                ]
            ),
            (
"""
segments:
  - start: 0
    end: 15
""",
                ValueError(),
            ),
        ]

        for entry in entries:
            data_yaml, expected = entry

            with patch('src.vidsegment.segmentloader.open', mock_open(read_data=data_yaml)):
                with self.subTest():
                    loader = SegmentLoader()

                    if isinstance(expected, Exception):
                        with self.assertRaises(type(expected)):
                            loader.load_yaml('test')
                        continue

                    segments = loader.load_yaml('test')

                    self.assertEqual(len(expected), len(segments))

                    for i in range(len(expected)):
                        self.assertEqual(expected[i]['start'], segments[i].start)
                        self.assertEqual(expected[i]['end'], segments[i].end)
                        self.assertEqual(expected[i]['filename'], segments[i].filename)
                        self.assertEqual(expected[i]['title'], segments[i].title)
                        self.assertEqual(expected[i]['volume'], segments[i].volume)

                        if expected[i]['metadata'] is not None:
                            self.assertDictEqual(expected[i]['metadata'], segments[i].metadata)
                        else:
                            self.assertIsNone(segments[i].metadata)
