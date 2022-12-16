import os
import importlib
import glob
import json
import sys
from typing import List
from types import FunctionType

from testing.test import TestPack, TestType, Test


def get_in_tests(alltests: FunctionType | None, test_dir: str, program: str, time_limit: float):
    """Get .in tests."""

    packs = []

    for pack_dir in os.listdir(test_dir):
        if not os.path.isdir(os.path.join(test_dir, pack_dir)) or pack_dir == '__pycache__':
            continue
        pack_name = os.path.basename(pack_dir)
        pack_tests = []
        sys.path.append(os.path.join(test_dir, pack_dir))
        for x in glob.glob(os.path.join(pack_dir, '*.in')):
            name = os.path.basename(x)[:-3]

            # Read the input
            with open(x, 'r') as f:
                test_input = f.read()

            if os.path.isfile(x[:-3] + '.out'):
                # We have a static .in/.out test
                # Read the output
                with open(x[:-3] + '.out', 'r') as f:
                    test_output = f.read()

                pack_tests.append(Test(program, name + '#in/out',
                                       TestType.STATIC, test_input, test_output, time_limit))
            if os.path.isfile(x[:-3] + '.py'):
                # We have a checker .in/.py test
                # Import the checker
                checker = importlib.import_module(name).test

                pack_tests.append(Test(program, name + '#in/py',
                                       TestType.CHECKER, test_input, checker, time_limit))
            if alltests is not None:
                # We have a checker ALLTESTS.py test

                pack_tests.append(Test(program, name + '#in/atpy',
                                       TestType.CHECKER, test_input, alltests, time_limit))
        sys.path.pop()
        packs.append(TestPack(pack_name, pack_tests))

    return packs


def get_json_tests(alltests: FunctionType | None, test_dir: str, program: str, time_limit: float):
    """Get TESTS.json tests."""

    packs = []

    if os.path.isfile(os.path.join(test_dir, 'TESTS.json')):
        with open(os.path.join(test_dir, 'TESTS.json'), 'r') as f:
            file = json.load(f)

        for pack_name, tests in file.items():
            pack_tests = []
            # key is the test name, value is an array with the input and optional output
            for name, test in tests.items():
                if len(test) == 1 and alltests is not None:
                    # We have a checker TESTS.json test
                    pack_tests.append(Test(program, name + '#json/atpy',
                                           TestType.CHECKER, test[0], alltests, time_limit))
                elif len(test) == 2:
                    # We have a static TESTS.json test
                    pack_tests.append(Test(program, name + '#json',
                                           TestType.STATIC, test[0], test[1], time_limit))
            packs.append(TestPack(pack_name, pack_tests))

    return packs


def get_generator_tests(alltests: FunctionType | None, test_dir: str, program: str, time_limit: float):
    """Run GENERATOR.py if it exists"""
    packs = []

    if os.path.isfile(os.path.join(test_dir, 'GENERATOR.py')):
        generator = importlib.import_module('GENERATOR').generate
        for pack_name, generated_tests in generator().items():
            pack_tests = []
            for name, test_type, test in generated_tests:
                if test_type == TestType.STATIC.value:
                    inp, outp = test
                    pack_tests.append(Test(program, name + '#gen',
                                           TestType.STATIC, inp, outp, time_limit))
                elif test_type == TestType.CHECKER.value and alltests is not None:
                    inp = test
                    pack_tests.append(Test(program, name + '#gen/atpy',
                                           TestType.CHECKER, inp, alltests, time_limit))
            packs.append(TestPack(pack_name, pack_tests))

    return packs


def get_tests(test_dir: str, program: str, time_limit: float) -> List[TestPack]:
    # Import ALLTESTS.py if it exists
    alltests = None
    if os.path.isfile(os.path.join(test_dir, 'ALLTESTS.py')):
        alltests = importlib.import_module('ALLTESTS').test

    packs = []

    packs.extend(get_in_tests(alltests, test_dir, program, time_limit))
    packs.extend(get_json_tests(alltests, test_dir, program, time_limit))
    packs.extend(get_generator_tests(alltests, test_dir, program, time_limit))

    return packs
