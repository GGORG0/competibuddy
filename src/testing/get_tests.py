import os
import importlib
import glob
import json

from testing.test_types import TestType


def get_in_tests(alltests, test_dir):
    """Get .in tests."""

    tests = {}

    for x in glob.glob(os.path.join(test_dir, '*.in')):
        name = os.path.basename(x)[:-3]

        # Read the input
        with open(x, 'r') as f:
            test_input = f.read()

        if os.path.isfile(x[:-3] + '.out'):
            # We have a static .in/.out test
            # Read the output
            with open(x[:-3] + '.out', 'r') as f:
                test_output = f.read()

            tests[name + '#in/out'] = (TestType.STATIC,
                                       test_input, test_output)
        if os.path.isfile(x[:-3] + '.py'):
            # We have a checker .in/.py test
            # Import the checker
            checker = importlib.import_module(name).test

            tests[name + '#in/py'] = (TestType.CHECKER, test_input, checker)
        if alltests is not None:
            # We have a checker ALLTESTS.py test

            tests[name + '#in/atpy'] = (TestType.CHECKER, test_input, alltests)

    return tests


def get_json_tests(alltests, test_dir):
    """Get TESTS.json tests."""

    tests = {}

    if os.path.isfile(os.path.join(test_dir, 'TESTS.json')):
        with open(os.path.join(test_dir, 'TESTS.json'), 'r') as f:
            file = json.load(f)

        # key is the test name, value is an array with the input and optional output
        for name, test in file.items():
            if len(test) == 1:
                # We have a checker TESTS.json test
                tests[name +
                      '#json/atpy'] = (TestType.CHECKER, test[0], alltests)
            elif len(test) == 2:
                # We have a static TESTS.json test
                tests[name + '#json'] = (TestType.STATIC, test[0], test[1])

    return tests


def get_generator_tests(alltests, test_dir):
    """Run GENERATOR.py if it exists"""
    tests = {}

    if os.path.isfile(os.path.join(test_dir, 'GENERATOR.py')):
        generator = importlib.import_module('GENERATOR').generate
        for name, test_type, test in generator():
            if test_type == TestType.STATIC.value:
                inp, outp = test
                tests[name + '#gen'] = (TestType.STATIC, inp, outp)
            elif test_type == TestType.CHECKER.value:
                inp = test
                tests[name + '#gen/atpy'] = (TestType.CHECKER, inp, alltests)

    return tests


def get_tests(test_dir):
    # Import ALLTESTS.py if it exists
    alltests = None
    if os.path.isfile(os.path.join(test_dir, 'ALLTESTS.py')):
        alltests = importlib.import_module('ALLTESTS').test

    # { name: (type, input, output) } where type is test_types.TestType
    tests = {}

    tests.update(get_in_tests(alltests, test_dir))
    tests.update(get_json_tests(alltests, test_dir))
    tests.update(get_generator_tests(alltests, test_dir))

    return tests
