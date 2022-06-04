from enum import Enum
import platform
import re
from typing import Dict, Optional

class System(str, Enum):
    UNKNOWN = 'unknown'
    LINUX = 'linux'
    WINDOWS = 'windows'
    DARWIN = 'darwin'

class FilenameSlug:
    def __init__(self, system: Optional[str] = None):
        self._system: System = _get_system(
            system if system is not None else platform.system()
        )

    def slug_filename(self, filename: str) -> str:
        if self._system == System.LINUX:
            return self._slug_filename_linux(filename)
        if self._system == System.WINDOWS:
            return self._slug_filename_windows(filename)
        raise ValueError(f'unsupported system: {self._system}')

    def _replace_chars(self, string: str, replace: Dict[str, str]) -> str:
        return ''.join(replace.get(char, char) for char in string)

    def _slug_filename_linux(self, filename: str) -> str:
        filename = self._replace_chars(filename, {
            '/': '\u2215',
        })

        if filename == '.':
            filename = '\u00b7'
        elif filename == '..':
            filename = '\u00b7\u00b7'

        return filename

    def _slug_filename_windows(self, filename: str) -> str:
        filename = self._replace_chars(filename, {
            '<': '\uff1c',
            '>': '\uff1e',
            ':': '\uff1a',
            '"': '\u201c',
            '/': '\u2215',
            '\\': '\uff3c',
            '|': '\uff5c',
            '?': '\uff1f',
            '*': '\uff0a',
        })

        if filename == '.':
            filename = '\u00b7'
        elif filename == '..':
            filename = '\u00b7\u00b7'

        match = re.fullmatch(r'CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9]', filename)
        if match is not None:
            filename += '_'

        return filename

def _get_system(system: Optional[str]) -> System:
    if system is None:
        return System.UNKNOWN
    if system.lower() == 'linux':
        return System.LINUX
    if system.lower() == 'windows':
        return System.WINDOWS
    if system.lower() == 'darwin':
        return System.DARWIN
    return System.UNKNOWN
