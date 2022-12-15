import os


def get_time_limit(test_dir, time_limit):
    if time_limit is not None:
        return float(time_limit)

    if os.path.isfile(os.path.join(test_dir, 'TIME_LIMIT')):
        with open(os.path.join(test_dir, 'TIME_LIMIT'), 'r') as f:
            return float(f.read())

    return 0
