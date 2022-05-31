import re

def time_to_seconds(time: str) -> float:
    match = re.fullmatch(r'(?:(?:(?P<hours>[0-9]+):)?(?P<minutes>[0-5]?[0-9]):)?(?P<seconds>[0-5]?[0-9](?:\.[0-9]*)?)', time)
    if match is None:
        raise ValueError('invalid time format')

    def _get(d: dict, key: str, default: str) -> str:
        result = d.get(key)
        return result if result is not None else default

    groups = match.groupdict()
    return int(_get(groups, 'hours', '0')) * 3600 + int(_get(groups, 'minutes', '0')) * 60 + float(_get(groups, 'seconds', '0'))
