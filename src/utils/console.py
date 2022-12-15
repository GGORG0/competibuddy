import colorama
import sys

icons = {
    "success": "✓",
    "error": "✗",
    "warning": "⚠",
    "question": "?",
    "bullet": "•",
    "pointer": "❯",
    "pointer_small": "›",
}


# Errors

def error(text, exit_program=False):
    print(colorama.Fore.RED + text + colorama.Style.RESET_ALL)
    if exit_program:
        sys.exit(1)


def error_icon(text, exit_program=False):
    error(f"{icons['error']} {text}",  exit_program)


def error_message(text, exit_program=True):
    error_icon(f"ERROR: {text}", exit_program)


# Warnings

def warning(text):
    print(colorama.Fore.YELLOW + text + colorama.Style.RESET_ALL)


def warning_icon(text):
    warning(f"{icons['warning']} {text}")


def warning_message(text):
    warning_icon(f"WARNING: {text}")


# Success

def success(text):
    print(colorama.Fore.GREEN + text +
          colorama.Style.RESET_ALL)


def success_icon(text):
    success(f"{icons['success']} {text}")


def success_message(text, newline=True):
    success_icon(f"SUCCESS: {text}")


# Info

def info(text):
    print(colorama.Fore.CYAN + text + colorama.Style.RESET_ALL)


def info_message(text):
    info(f"INFO: {text}")


# In progress

def in_progress(text, newline=False):
    print(colorama.Fore.YELLOW + text +
          colorama.Style.RESET_ALL + " ", end=("\n" if newline else ""))
