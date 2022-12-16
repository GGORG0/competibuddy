from typing import List
import argh
import os
import sys
import utils.console as console
import testing.get_tests as get_tests
import testing.get_time_limit as get_time_limit
import testing.compile as compile
import testing.test as libtest
import colorama


def init_checks(program, test_dir):
    # Check if the provided file exists.
    if not os.path.exists(program):
        raise FileNotFoundError(f"File not found: {program}")
    program = os.path.abspath(program)

    # Check if the provided test directory exists.
    if test_dir != "" and not os.path.exists(test_dir):
        raise FileNotFoundError(f"Test directory not found: {test_dir}")

    # If no test directory was provided, use the parent directory of the program.
    if test_dir == "":
        console.info_message(
            "No test directory provided. Using the parent directory of the program.")
        test_dir = os.path.dirname(program)

    # Add the test directory to the PATH.
    sys.path.insert(1, test_dir)

    return program, test_dir


def summary(packs_passed: int, packs: List[libtest.TestPack], tests_passed: int, test_count: int):
    print()
    print(colorama.Fore.CYAN + '=== Summary ===' + colorama.Style.RESET_ALL)
    if packs_passed == len(packs):
        console.success_icon('All tests passed!')
    else:
        console.error_icon(
            f'Passed {packs_passed} out of {len(packs)} packs ({round(packs_passed/len(packs)*100)}%).')
        console.error(
            f'  That\'s {tests_passed} out of {test_count} tests ({round(tests_passed/test_count*100)}%).')
        for i, pack in enumerate(packs, start=1):
            if len(pack) == 0 or pack.passed_tests == -1:
                continue
            if pack.passed_tests == len(pack):
                console.success_icon(f'{i} {console.icons["pointer"]} {pack}')
            else:
                console.error_icon(f'{i} {console.icons["pointer"]} {pack}')



@argh.arg("program", help="The program to test. Can be an executable or a C++ source file (will be compiled).")
@argh.arg("--test-dir", help="The directory containing the tests. Defaults to the parent directory of the program.")
@argh.arg("--time-limit", help="The time limit for each test in seconds. Defaults to unlimited (0). Can also be provided in a file named TIMELIMIT.txt in the test directory.")
def test(program: str, test_dir: str = "", time_limit: float = 0):
    """Run tests on the specified program."""

    program, test_dir = init_checks(program, test_dir)
    program = compile.compile_file(program)
    time_limit = get_time_limit.get_time_limit(test_dir, time_limit)
    packs = get_tests.get_tests(test_dir, program, time_limit)
    print()
    passed_packs, pack_count, passed_tests, test_count = libtest.run_packs(
        packs)
    summary(passed_packs, packs, passed_tests, test_count)
