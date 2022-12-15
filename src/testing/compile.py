import subprocess
import os
import utils.console as console


def compile_cpp(filename):
    """Compile a C++ file."""
    subprocess.run(["g++", "-o", filename[:-4], filename], check=True)
    return filename[:-4]


compilers = {
    ".cpp": compile_cpp
}


def compile_file(filename):
    """Compile the specified file."""
    console.in_progress(f"Compiling {filename}...")
    try:
        filename = compilers[os.path.splitext(filename)[1]](filename)
    except KeyError:
        print()
        console.warning_message(
            f"Unknown file type: {filename}. Running directly as executable.")
    except Exception:
        print()
        console.error_message(f"Failed to compile {filename}.")
        raise
    console.success_icon(f"Done!")
    return filename
