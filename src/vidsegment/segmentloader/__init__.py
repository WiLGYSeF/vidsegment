from typing import List

import yaml

from ..segment import Segment
from ..utils.time_to_seconds import time_to_seconds

class SegmentLoader:
    def load_yaml(self, filename: str) -> List[Segment]:
        with open(filename, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file.read())

        filename_template = data.get('filename')
        volume = data.get('volume')
        constant_rate_factor = data.get('constant_rate_factor')
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

            if start >= end:
                raise ValueError(f'start must be less than end: {start} and {end}')

            segment_filename = segment.get('filename', filename_template)
            if segment_filename is None:
                raise ValueError('no filename for segment')

            segment_volume = segment.get('volume', volume)
            if segment_volume is not None:
                segment_volume = str(segment_volume)

            segment_constant_rate_factor = segment.get('constant_rate_factor', constant_rate_factor)
            if segment_constant_rate_factor is not None:
                segment_constant_rate_factor = int(segment_constant_rate_factor)

            segments.append(Segment(
                start,
                end,
                segment_filename,
                segment.get('title'),
                segment_volume,
                segment_constant_rate_factor,
                segment.get('metadata', metadata),
            ))

        return segments
