# Competibuddy

Your competitive programming helper.

## Installation

1. Get Python
1. Get the repository (`git clone https://github.com/GGORG0/competibuddy.git`)
1. Install the requirements (`pip install -r requirements.txt`)
1. (optional) Add the `src` directory to your `PATH` environment variable if you want to use the `cbuddy` command from anywhere
1. Look at the usage by running `cbuddy --help` (or `python src/cbuddy.py --help` if you didn't add the `src` directory to your `PATH` environment variable)

## Tester module

The tester module is a simple tool to test your code against a set of test cases.

It looks for tests in the provided directory (`--test-dir` argument) or the parent directory of the program.

For now it only supports C++ programs and binary executables.

You can create a `TIMELIMIT.txt` file in the test directory to set a time limit for the program. The time limit is in seconds and can be a decimal number.

### Test types

- **`.in`/`.out`**
  Classic input/output tests. The tester will compare the output of your program with the expected output.
- **`.in`/`.py`**
  This will run the python file to test the output of your program. The python file should contain a function called `test` return a boolean value.
- **`.in`/`ALLTESTS.py`**
  Similar to the previous one, but the python file is the same for all tests.
- **`TESTS.json`**
  If the test cases are 1 line, you can provide them in a `json` file instead. Create a dictionary with the test name as the key and a list of the input and output as the value. The tester will run the program for each test and compare the output with the expected output.
- **`TESTS.json`/`ALLTESTS.py`**
  Similar to the previous one, but instead of comparing the output to a static value, it runs the `ALLTESTS.py` file to test the output. Then the dictionary value is just a 1-item list with the input.
- **`GENERATOR.py`/`ALLTESTS.py`**
  This will run the generator file to generate the test cases. The generator file should contain a function called `generate` that returns a list of tuples with the test name, test type (`2` - checker) and input. The tester will run the program for each test and compare the output with the expected output.
- **`GENERATOR.py`**
  Similar to the previous one, but instead of running a tester for each test case, the generator outputs a list of tuples with the test name, test type (`1` - static), input and output. The tester will compare the output of your program with the expected output.

## TODO

- Test packs - a way to group tests together by putting them in a nested directory (tester module)
- Other programming languages (tester module)
- Separate brute force program for checking the output of the program (tester module)
- Recursively find the program by just using its filename (tester module)
- Add a `--test` argument to run a single test (tester module)
- Online judge support module (uploading solutions, downloading test cases, etc.)
  - [Themis](https://themis.ii.uni.wroc.pl)
  - [SIO2](https://sio2.mimuw.edu.pl)
  - [Szkopuł](https://szkopul.edu.pl)
  - [Codeforces](https://codeforces.com)
  - [Solve.edu.pl](https://solve.edu.pl)
- `new` command to create a new problem directory with a template program and add an option to automatically download problem info, test cases and time limit from an online judge
