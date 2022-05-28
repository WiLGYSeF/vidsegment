#!/usr/bin/env python3

import os
import subprocess
import sys
from typing import Iterable, List, Optional

import yaml

class Segment:
    def __init__(self,
        start: float,
        end: float,
        title: str,
        filename: Optional[str] = None,
        origin: Optional[str] = None,
    ):
        self.start: float = start
        self.end: float = end
        self.title: str = title
        self.filename: Optional[str] = filename
        self.origin: Optional[str] = origin

def split_video(dest_path: str, filename: str, segments: Iterable[Segment], overwrite: bool = False) -> None:
    _, extension = os.path.splitext(filename)

    for segment in segments:
        dest_filename = segment.filename if segment.filename is not None else segment.title + extension
        dest_filepath = os.path.join(dest_path, dest_filename)

        arguments = ['ffmpeg', '-i', filename, '-c', 'copy', '-ss', str(segment.start), '-to', str(segment.end)]
        if overwrite:
            arguments.append('-y')
        else:
            arguments.append('-n')
        if segment.origin is not None:
            arguments.extend(['-metadata', f'comment={segment.origin}'])

        arguments.append(dest_filepath)

        os.makedirs(os.path.dirname(dest_filepath), exist_ok=True)

        result = subprocess.run(arguments)
        if result.returncode != 0:
            raise RuntimeError()

def load_segments(filename: str) -> List[Segment]:
    with open(filename, 'r') as file:
        data = yaml.safe_load(file.read())
    
    segments = []
    for segment in data['segments']:
        segments.append(Segment(
            segment['start'],
            segment['end'],
            segment['title'],
            segment.get('filename'),
            segment.get('origin'),
        ))

    return segments

if __name__ == '__main__':
    input_video = sys.argv[1]
    input_segments = sys.argv[2]
    output_path = sys.argv[3]

    segments = load_segments(input_segments)
    split_video(output_path, input_video, segments)
