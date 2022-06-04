#!/usr/bin/env python3

import os
import sys
from typing import List

from . import VERSION
from . import argscli
from .segmentloader import SegmentLoader
from .videosplitter import VideoSplitter

def main(args: List[str]):
    namespace, args = argscli.parse_args(args)

    if namespace.version:
        print(f'vidsegment v{VERSION}\n')

        try:
            os.system('ffmpeg -version')
        except Exception as exc:
            print(f'error: could not get ffmpeg version: {exc}')
        sys.exit(0)

    input_video = namespace.input
    input_segments = namespace.segment
    output_path = namespace.dest

    segmentloader = SegmentLoader()
    segments = segmentloader.load_yaml(input_segments)

    splitter = VideoSplitter()
    try:
        for result in splitter.split_video(
            input_video,
            output_path,
            segments,
            overwrite=namespace.overwrite,
            re_encode_video=namespace.re_encode,
            decode_before_seek=namespace.decode_before_seek,
            avoid_negative_ts=namespace.avoid_negative_ts,
            continue_on_fail=namespace.continue_on_fail,
            #verbose=namespace.verbose,
        ):
            if result.success:
                print(result.filename)
            else:
                print(result.result, file=sys.stderr)
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)

def main_args():
    main(sys.argv[1:])

if __name__ == '__main__':
    main_args()
