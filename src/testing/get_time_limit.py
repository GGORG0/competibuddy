import os


def get_time_limit(test_dir, time_limit):
    if time_limit is not None:
        return float(time_limit)

    if os.path.isfile(os.path.join(test_dir, 'TIMELIMIT.txt')):
        with open(os.path.join(test_dir, 'TIMELIMIT.txt'), 'r') as f:
            return float(f.read())

    return 0
