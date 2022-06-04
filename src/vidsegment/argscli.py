from argparse import ArgumentParser, Namespace
from typing import Iterable, List, Tuple

def _get_parser() -> ArgumentParser:
    parser = ArgumentParser(prog='vidsegment', description='Cut videos into segments.')
    parser.add_argument('-V', '--version', action='store_true', help='prints version and exits')
    parser.add_argument('-v', '--verbose', action='store_true', help='show ffmpeg output')

    parser.add_argument('-i', '--input', action='store', help='input file', required=True)
    parser.add_argument('-d', '--dest', action='store', help='output directory', required=True)
    parser.add_argument('-s', '--segment', action='store', help='segment config file', required=True)

    parser.add_argument('--overwrite', action='store_true', help='overwrite existing files')
    parser.add_argument('-c', '--copy', action='store_true', help='use ffmpeg -c copy')
    parser.add_argument('--continue-on-fail', action='store_true', help='continue in case of failure')

    return parser

def parse_args(args: Iterable[str]) -> Tuple[Namespace, List[str]]:
    return _get_parser().parse_known_args(args)

def print_help() -> None:
    _get_parser().print_help()