#!/usr/bin/env python3

import argh
import colorama

import testing.testing as testing
import utils.console as console


parser = argh.ArghParser()
parser.add_commands([testing.test])


def main():
    colorama.init()

    try:
        parser.dispatch()
    except Exception as e:
        console.error_message(str(e))


if __name__ == "__main__":
    main()
