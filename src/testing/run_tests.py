import subprocess
import time
from testing.test_types import TestType
import utils.console as console


class TimeLimitExceeded(Exception):
    time_limit: float = 0

    def __init__(self, time_limit):
        self.time_limit = time_limit

    def __str__(self):
        return f'Time limit ({self.time_limit}s) exceeded.'


class NonZeroExitCode(Exception):
    exit_code: int = 0
    program_output: str = ""

    def __init__(self, exit_code, program_output):
        self.exit_code = exit_code
        self.program_output = program_output.strip()

    def __str__(self):
        outp = f'Program exited with non-zero exit code {self.exit_code}.'
        if len(self.program_output) > 0 and len(self.program_output) < 100:
            outp += f"\nOutput:\n{self.program_output}\n"
        return outp


class WrongAnswer(Exception):
    test_input: str = ""
    test_output: str = ""
    actual_output: str = ""

    def __init__(self, test_input, actual_output, test_output=""):
        self.test_input = test_input.strip()
        self.actual_output = actual_output.strip()
        self.test_output = test_output.strip()

    def __str__(self):
        outp = "Wrong answer.\n"
        if len(self.test_input) > 0 and len(self.test_input) < 100:
            outp += f"Input:\n{self.test_input}\n"
        if len(self.test_output) > 0 and len(self.test_output) < 100:
            outp += f"Expected output:\n{self.test_output}\n"
        if len(self.actual_output) > 0 and len(self.actual_output) < 100:
            outp += f"Actual output:\n{self.actual_output}\n"
        return outp


def execute_program(program, test_input, time_limit):
    start_time = time.time()
    try:
        if time_limit is not None and time_limit > 0:
            proc = subprocess.run(
                [program],
                input=test_input,
                encoding='utf-8',
                stdout=subprocess.PIPE,
                timeout=time_limit,
                check=True)
        else:
            proc = subprocess.run(
                [program],
                input=test_input,
                encoding='utf-8',
                stdout=subprocess.PIPE,
                check=True)
    except subprocess.TimeoutExpired:
        raise TimeLimitExceeded(time_limit)
    except subprocess.CalledProcessError as err:
        raise NonZeroExitCode(err.returncode, err.stdout)

    run_time = time.time() - start_time
    return proc.stdout.strip(), run_time


def check_output(program_output, test_type, test_input, test_output):
    if test_type == TestType.STATIC:
        if program_output == test_output.strip():
            return True
        else:
            raise WrongAnswer(test_input, program_output, test_output)
    elif test_type == TestType.CHECKER:
        console.in_progress('Checking...')
        if test_output(test_input, program_output):
            return True
        else:
            raise WrongAnswer(test_input, program_output)


def run_tests(program, tests, time_limit):
    passed_tests = 0
    test_count = len(tests)
    for i, t in enumerate(tests.items(), start=1):
        name, test = t

        test_type, test_input, test_output = test
        console.in_progress(
            f'[{i}/{test_count}] Running {"checker" if test_type == TestType.CHECKER else "static"} test {name}...')

        try:
            actual_output, run_time = execute_program(
                program, test_input, time_limit)

            if check_output(actual_output, test_type, test_input, test_output):
                console.success_icon(f'Passed ({run_time:.3f}s)!')
                passed_tests += 1
        except Exception as e:
            console.error_icon(str(e))

    return passed_tests
