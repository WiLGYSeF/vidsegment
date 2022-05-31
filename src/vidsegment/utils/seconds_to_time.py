def seconds_to_time(seconds: float) -> str:
    result = ''
    for div in (3600, 60):
        remainder = int(seconds // div)
        if remainder > 0 or len(result) > 0:
            result += f'{remainder:02d}:'
        seconds %= div

    if len(result) == 0:
        result = '00:'

    if int(seconds) != seconds:
        seconds = round(seconds, 3)
    else:
        seconds = int(seconds)

    if seconds < 10:
        result += '0'
    result += str(seconds)
    return result
