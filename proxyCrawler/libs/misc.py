import contextlib
import json
import os

import time


@contextlib.contextmanager
def stopwatch(message):
    """Context manager to print how long a block of code took."""
    t0 = time.time()
    try:
        yield
    finally:
        t1 = time.time()
        print('Total elapsed time for %s: %.3f' % (message, t1 - t0))


def save_to_json(data, filePath):
    with open(filePath, 'w') as fd:
        json.dump(data, fd)


def load_from_json(filePath):
    if os.path.isfile(filePath):
        with open(filePath, 'r') as fd:
            data = json.load(fd)
    else:
        data = []
    return data