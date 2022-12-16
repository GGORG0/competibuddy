#!/usr/bin/env python3

import argh
import colorama

import testing.testing as testing
import utils.console as console


parser = argh.ArghParser()
parser.add_commands([testing.test])


def main():
    colorama.init()

    parser.dispatch()


if __name__ == "__main__":
    main()
