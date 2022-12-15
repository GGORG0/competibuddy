import argh
import os
import sys
import utils.console as console
import testing.get_tests as get_tests
import testing.get_time_limit as get_time_limit
import testing.run_tests as run_tests
import testing.compile as compile


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


def summary(passed, total):
    print()
    if passed == total:
        console.success_icon('All tests passed!')
    else:
        console.error_icon(
            f'Passed {passed} out of {total} tests ({round(passed/total*100)}%).')


@argh.arg("program", help="The program to test. Can be an executable or a C++ source file (will be compiled).")
@argh.arg("--test-dir", help="The directory containing the tests. Defaults to the parent directory of the program.")
@argh.arg("--time-limit", help="The time limit for each test in seconds. Defaults to unlimited (0). Can also be provided in a file named TIMELIMIT.txt in the test directory.")
def test(program: str, test_dir: str = "", time_limit: float = 0):
    """Run tests on the specified program."""

    program, test_dir = init_checks(program, test_dir)
    program = compile.compile_file(program)
    tests = get_tests.get_tests(test_dir)
    time_limit = get_time_limit.get_time_limit(test_dir, time_limit)
    print()
    passed = run_tests.run_tests(program, tests, time_limit)
    summary(passed, len(tests))
