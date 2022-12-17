import enum
import time
import subprocess
from types import FunctionType
from typing import List

import utils.console as console


class TesterException(Exception):
    pass


class TimeLimitExceeded(TesterException):
    time_limit: float = 0

    def __init__(self, time_limit):
        self.time_limit = time_limit

    def __str__(self):
        return f'Time limit ({self.time_limit}s) exceeded.'


class NonZeroExitCode(TesterException):
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


class WrongAnswer(TesterException):
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


class TestType(enum.Enum):
    STATIC = 1
    CHECKER = 2


class Test():
    def __init__(self, program: str, name: str, test_type: TestType, stdin: str, stdout_or_checker: str | FunctionType, time_limit: float = 0):
        if test_type == TestType.CHECKER and not callable(stdout_or_checker):
            raise ValueError(
                "stdout_or_checker must be a function if test_type is CHECKER")
        elif test_type == TestType.STATIC and callable(stdout_or_checker):
            raise ValueError(
                "stdout_or_checker must be a string if test_type is STATIC")

        self.program = program
        self.name = name
        self.test_type = test_type
        self.stdin = stdin
        self.stdout_or_checker = stdout_or_checker
        self.time_limit = time_limit

    def __str__(self):
        return self.name

    def execute(self):
        start_time = time.time()
        try:
            if self.time_limit is not None and self.time_limit > 0:
                proc = subprocess.run(
                    [self.program],
                    input=self.stdin,
                    encoding='utf-8',
                    stdout=subprocess.PIPE,
                    timeout=self.time_limit,
                    check=True)
            else:
                proc = subprocess.run(
                    [self.program],
                    input=self.stdin,
                    encoding='utf-8',
                    stdout=subprocess.PIPE,
                    check=True)
        except subprocess.TimeoutExpired:
            raise TimeLimitExceeded(self.time_limit)
        except subprocess.CalledProcessError as err:
            raise NonZeroExitCode(err.returncode, err.stdout)

        run_time = time.time() - start_time
        return proc.stdout.strip(), run_time

    def check_output(self, output):
        if self.test_type == TestType.STATIC and not callable(self.stdout_or_checker):
            if output == self.stdout_or_checker.strip():
                return True
            else:
                raise WrongAnswer(self.stdin, output,
                                  self.stdout_or_checker)  # type: ignore
        elif self.test_type == TestType.CHECKER and callable(self.stdout_or_checker):
            console.in_progress('Checking...')
            try:
                if self.stdout_or_checker(self.stdin, output):
                    return True
                else:
                    raise WrongAnswer(self.stdin, output)
            except AssertionError as e:
                raise WrongAnswer(self.stdin, output, str(e))

    def run(self):
        try:
            actual_output, run_time = self.execute()

            if self.check_output(actual_output):
                console.success_icon(f'Passed ({run_time:.3f}s)!')
                return True
            else:
                if callable(self.stdout_or_checker):
                    raise WrongAnswer(self.stdin, actual_output)
                else:
                    raise WrongAnswer(self.stdin, actual_output,
                                      self.stdout_or_checker)  # type: ignore
        except TesterException as e:
            console.error_icon(str(e))
            return False


class TestPack(List[Test]):
    name: str = ""
    passed_tests: int = -1
    ran_tests: int = -1

    def __init__(self, name: str, tests: List[Test]):
        self.name = name
        super().__init__(tests)

    def summary(self):
        if self.ran_tests < len(self):
            console.warning_icon(
                f'[{self.name}] Ran only {self.ran_tests} out of {len(self)} tests.')
        if self.passed_tests == self.ran_tests:
            console.success_icon(f'[{self.name}] All tests passed!')
        else:
            console.error_icon(
                f'[{self.name}] Passed {self.passed_tests} out of {self.ran_tests} tests ({round(self.passed_tests/self.ran_tests*100)}%).')

    def run(self):
        self.passed_tests = 0
        self.ran_tests = 0
        try:
            for i, test in enumerate(self, start=1):
                console.in_progress(
                    f' {console.icons["pointer"]} [{self.name}: {i}/{self.ran_tests}] Running {"checker" if test.test_type == TestType.CHECKER else "static"} test {test.name}...')
                if test.run():
                    self.passed_tests += 1
                self.ran_tests += 1
        except KeyboardInterrupt:
            print()
            console.error_icon('Interrupted!')
        self.summary()
        return self.passed_tests, self.ran_tests

    def __str__(self):
        if self.passed_tests > 0 and self.ran_tests > 0:
            return f"{self.name} ({self.passed_tests}/{self.ran_tests} - {round(self.passed_tests/self.ran_tests*100)}% tests passed)"
        else:
            return f"{self.name} ({self.ran_tests} tests)"


def run_packs(packs: List[TestPack]):
    passed_packs = 0
    passed_tests = 0
    pack_count = len(packs)
    test_count = 0
    for i, pack in enumerate(packs, start=1):
        if len(pack) == 0:
            continue
        print()
        console.in_progress(
            f'[{i}/{pack_count}] Running test pack {pack.name}...', True)

        pack_passed_tests, pack_ran_tests = pack.run()
        test_count += pack_ran_tests
        passed_tests += pack_passed_tests
        if pack_passed_tests == pack_ran_tests:
            passed_packs += 1

    return passed_packs, pack_count, passed_tests, test_count
