#!/usr/bin/env python3

import sys
from typing import List

from .segmentloader import SegmentLoader
from .videosplitter import VideoSplitter

def main(args: List[str]):
    # TODO: argparse

    input_video = args[0]
    input_segments = args[1]
    output_path = args[2]

    segmentloader = SegmentLoader()
    segments = segmentloader.load_yaml(input_segments)

    splitter = VideoSplitter()
    for result in splitter.split_video(input_video, output_path, segments):
        if result.success:
            print(result.filename)
        else:
            print(result.result, file=sys.stderr)

def main_args():
    main(sys.argv[1:])

if __name__ == '__main__':
    main_args()
