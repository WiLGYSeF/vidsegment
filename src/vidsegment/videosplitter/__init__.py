import os
from string import Template
import subprocess
import sys
from typing import Dict, Generator, Iterable

from ..filename_slug import FilenameSlug
from ..segment import Segment
from ..utils.seconds_to_time import seconds_to_time

class VideoSplitResult:
    def __init__(self,
        success: bool,
        result: str,
        filename: str
    ):
        self.success: bool = success
        self.result: str = result
        self.filename: str = filename

class VideoSplitter:
    def split_video(self,
        filename: str,
        dest_path: str,
        segments: Iterable[Segment],
        overwrite: bool = False,
        re_encode_video: bool = False,
        decode_before_seek: bool = False,
        avoid_negative_ts: bool = False,
        continue_on_fail: bool = False,
        verbose: bool = False,
    ) -> Generator[VideoSplitResult, None, None]:
        _, extension = os.path.splitext(filename)
        extension = extension.lstrip('.')

        for segment in segments:
            substitutions = self._get_substitutions(segment, extension)

            dest_filename = FilenameSlug().slug_filename(
                Template(segment.filename).substitute(substitutions)
            )
            dest_filepath = os.path.join(dest_path, dest_filename)

            arguments = [
                'ffmpeg',
                '-y' if overwrite else '-n',
            ]

            if decode_before_seek:
                arguments.extend([
                    '-i', filename,
                    '-ss', str(segment.start),
                    '-to', str(segment.end),
                ])
            else:
                arguments.extend([
                    '-ss', str(segment.start),
                    '-to', str(segment.end),
                    '-i', filename,
                ])

            if not re_encode_video:
                if segment.volume is not None:
                    arguments.extend(['-c:v', 'copy'])
                else:
                    arguments.extend(['-c', 'copy'])
            if avoid_negative_ts:
                arguments.extend(['-avoid_negative_ts', '1'])
            if segment.volume is not None:
                arguments.extend(['-af', f'volume={segment.volume}'])
            if segment.constant_rate_factor is not None:
                arguments.extend(['-crf', str(segment.constant_rate_factor)])
            if segment.title is not None:
                arguments.extend(['-metadata', f'title={segment.title}'])
            if segment.metadata is not None:
                for key, val in segment.metadata.items():
                    arguments.extend(['-metadata', f'{key}={Template(val).safe_substitute(substitutions)}'])

            # TODO: segment artists, album

            arguments.append(dest_filepath)

            os.makedirs(os.path.dirname(dest_filepath), exist_ok=True)

            # TODO: verbose mode

            with subprocess.Popen(
                arguments,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            ) as process:
                _, stderr = process.communicate()
                if process.returncode != 0:
                    if not continue_on_fail:
                        raise RuntimeError(stderr.decode('utf-8'))
                    yield VideoSplitResult(False, stderr.decode('utf-8'), dest_filepath)
                else:
                    yield VideoSplitResult(True, '', dest_filepath)

    def _get_substitutions(self,
        segment: Segment,
        extension: str,
    ) -> Dict[str, str]:
        substitutions = {
            'start': seconds_to_time(segment.start),
            'start_sec': str(segment.start),
            'end': seconds_to_time(segment.end),
            'end_sec': str(segment.end),
            'duration': seconds_to_time(segment.start - segment.end),
            'duration_sec': str(segment.start - segment.end),
            'extension': extension,
        }

        if segment.title is not None:
            substitutions['title'] = segment.title

        if segment.metadata is not None:
            for key, val in segment.metadata.items():
                if key not in substitutions:
                    substitutions[key] = val

        return substitutions
