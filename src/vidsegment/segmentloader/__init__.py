from typing import List

import yaml

from ..segment import Segment
from ..utils.time_to_seconds import time_to_seconds

class SegmentLoader:
    def load_yaml(self, filename: str) -> List[Segment]:
        with open(filename, 'r') as file:
            data = yaml.safe_load(file.read())

        filename_template = data.get('filename')
        volume = data.get('volume')
        metadata = data.get('metadata')

        segments = []
        for segment in data['segments']:
            if ':' in segment['start']:
                start = time_to_seconds(segment['start'])
            else:
                start = float(segment['start'])

            if ':' in segment['end']:
                end = time_to_seconds(segment['end'])
            else:
                end = float(segment['end'])

            segments.append(Segment(
                start,
                end,
                segment['title'],
                segment.get('filename', filename_template),
                segment.get('volume', volume),
                segment.get('metadata', metadata),
            ))

        return segments
