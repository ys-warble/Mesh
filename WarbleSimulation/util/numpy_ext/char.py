import re

import numpy as np


def mod(format, tu_arrays):
    supported_formats = r'(%d|%s)'

    # 1. Check validity
    format_len = len(re.findall(supported_formats, format))
    if format_len != len(tu_arrays):
        raise ValueError('Different number of formats and tuple')
    elif format_len == 0 and len(tu_arrays) == 0:
        return None

    shape = tu_arrays[0].shape
    for arr in tu_arrays:
        if arr.shape != shape:
            raise ValueError('Tuple of arrays do not have uniform shape')

    # 2. Do algorithm
    shape = tu_arrays[0].shape
    formats = re.split(supported_formats, format)

    # check how many format and compare to how many arrays in the tuple

    result = None
    f_count = 0
    for f in formats:
        if result is None:
            result = np.full(shape, f)
            continue

        if re.match(supported_formats, f):
            result = np.char.add(result, np.char.mod(f, tu_arrays[f_count]))
            f_count += 1
        else:
            result = np.char.add(result, np.full(shape, f))

    # 3. Return result
    return result
