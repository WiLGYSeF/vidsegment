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
            if isinstance(segment['start'], str) and ':' in segment['start']:
                start = time_to_seconds(segment['start'])
            else:
                start = float(segment['start'])

            if isinstance(segment['end'], str) and ':' in segment['end']:
                end = time_to_seconds(segment['end'])
            else:
                end = float(segment['end'])

            segment_filename = segment.get('filename', filename_template)
            if segment_filename is None:
                raise ValueError('no filename for segment')

            segment_volume = segment.get('volume', volume)
            if segment_volume is not None:
                segment_volume = str(segment_volume)

            segments.append(Segment(
                start,
                end,
                segment_filename,
                segment.get('title'),
                segment_volume,
                segment.get('metadata', metadata),
            ))

        return segments
