#!/usr/bin/env python3

import os
import subprocess
import sys
from typing import Collection, Iterable, List, Optional

import yaml

from utils.time_to_seconds import time_to_seconds

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

def split_video(
    dest_path: str,
    filename: str,
    segments: Iterable[Segment],
    overwrite: bool = False
) -> None:
    _, extension = os.path.splitext(filename)

    # TODO: audio-only option
    # TODO: print stdout option
    # TODO: metadata

    for segment in segments:
        dest_filename = segment.filename if segment.filename is not None else segment.title + extension
        dest_filepath = os.path.join(dest_path, dest_filename)

        # TODO: optimize?

        arguments = [
            'ffmpeg',
            '-i', filename,
            '-c', 'copy',
            '-ss', str(segment.start),
            '-to', str(segment.end),
            '-y' if overwrite else '-n',
        ]
        if segment.origin is not None:
            arguments.extend(['-metadata', f'comment={segment.origin}'])

        arguments.append(dest_filepath)

        os.makedirs(os.path.dirname(dest_filepath), exist_ok=True)

        with subprocess.Popen(arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
            _, stderr = process.communicate()
            if process.returncode != 0:
                print(stderr.decode('utf-8'), file=sys.stderr)
                # TODO: aggregate exception option
                raise RuntimeError()

            # TODO: better output

            print(f'Wrote "{escape_quote(segment.title)}": {dest_filepath}')

def load_segments(filename: str) -> List[Segment]:
    with open(filename, 'r') as file:
        data = yaml.safe_load(file.read())

    origin = data.get('origin')

    # TODO: segment
    """
    prefix: value
    suffix: value
    filename: template
    metadata:
      - key: value
    """

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
            segment.get('filename'),
            segment.get('origin', origin),
        ))

    return segments

def escape_quote(string: str) -> str:
    return string.replace('\\', '\\\\').replace('"', '\\"')

def main(args: Collection[str]):
    input_video = args[0]
    input_segments = args[1]
    output_path = args[2]

    # TODO: template output filename

    segments = load_segments(input_segments)
    split_video(output_path, input_video, segments)

def main_args():
    main(sys.argv[1:])

if __name__ == '__main__':
    main_args()
