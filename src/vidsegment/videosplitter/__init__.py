import os
from string import Template
import subprocess
from typing import Dict, Generator, Iterable

from ..segment import Segment
from ..utils.seconds_to_time import seconds_to_time

SEEK_OFFSET = 5

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
        copy_video: bool = False,
        continue_on_fail: bool = False,
    ) -> Generator[VideoSplitResult, None, None]:
        _, extension = os.path.splitext(filename)
        extension = extension.lstrip('.')

        for segment in segments:
            substitutions = self._get_substitutions(segment, extension)

            # TODO: legalize filenames?
            dest_filename = Template(segment.filename).substitute(substitutions)
            dest_filepath = os.path.join(dest_path, dest_filename)

            # TODO: optimize?

            arguments = [
                'ffmpeg',
                '-ss', str(segment.start),
                '-to', str(segment.end),
                '-i', filename,
                '-y' if overwrite else '-n',
            ]
            if segment.volume is not None:
                arguments.extend(['-af', f'volume={segment.volume}'])
            if segment.constant_rate_factor is not None:
                arguments.extend(['-crf', str(segment.constant_rate_factor)])
            if segment.title is not None:
                arguments.extend(['-metadata', f'title={segment.title}'])
            if segment.metadata is not None:
                for key, val in segment.metadata.items():
                    arguments.extend(['-metadata', f'{key}={Template(val).safe_substitute(substitutions)}'])
            if copy_video:
                arguments.extend(['-c', 'copy'])

            arguments.append(dest_filepath)

            os.makedirs(os.path.dirname(dest_filepath), exist_ok=True)

            with subprocess.Popen(
                arguments,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            ) as process:
                _, stderr = process.communicate()
                if process.returncode != 0:
                    if not continue_on_fail:
                        raise RuntimeError(stderr)
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
