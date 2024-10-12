import argparse
import sys


def command1():
    print("Executing command1")


def command2():
    print("Executing command2")


def entrypoint():
    parser = argparse.ArgumentParser(description="bootstr's cli")

    subparsers = parser.add_subparsers(title="commands")

    parser_command1 = subparsers.add_parser("command1", help="Execute Command 1")
    parser_command1.set_defaults(func=command1)

    parser_command2 = subparsers.add_parser("command2", help="Execute Command 2")
    parser_command2.set_defaults(func=command2)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func()
