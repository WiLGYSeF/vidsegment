import os
from string import Template
import subprocess
from typing import Generator, Iterable

from ..segment import Segment

SEEK_OFFSET = 5

class VideoSplitResult:
    def __init__(self,
        success: bool,
        result: str,
        filename: str
    ):
        self.success: bool = success
        self.result: str = result,
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
            substitutions = {
                'start': segment.start,
                'end': segment.end,
                'duration': segment.start - segment.end,
                'title': segment.title,
                'extension': extension,
            }

            for key, val in segment.metadata.items():
                if key not in substitutions:
                    substitutions[key] = val

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
            if segment.metadata is not None:
                for key, val in segment.metadata.items():
                    arguments.extend(['-metadata', f'{key}={val}'])
            if copy_video:
                arguments.extend(['-c', 'copy'])

            arguments.append(dest_filepath)

            os.makedirs(os.path.dirname(dest_filepath), exist_ok=True)

            with subprocess.Popen(arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
                _, stderr = process.communicate()
                if process.returncode != 0:
                    if not continue_on_fail:
                        raise RuntimeError(stderr)
                    yield VideoSplitResult(False, stderr, dest_filepath)
                else:
                    yield VideoSplitResult(True, '', dest_filepath)
