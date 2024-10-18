from __future__ import annotations

import argparse
import pathlib
import sys

from importlib_metadata import version

from .core import run

ITERATIONS_DEFAULT = 50
EXTRA_DEFAULT = 1
COLOR_DEFAULT = 1.0
OUTPUT_DEFAULT = None

PROGRAM = "pycrusher"


def get_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=PROGRAM)
    parser.add_argument(
        "input_path",
        type=pathlib.Path,
        help="Input image filename",
        metavar="INPUT_PATH",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {version(PROGRAM)}",
        help="show %(prog)s version",
    )

    parser.add_argument(
        "-i",
        "--iterations",
        dest="iterations",
        type=int,
        help="Number of compression iterations",
        default=ITERATIONS_DEFAULT,
    )
    parser.add_argument(
        "-e",
        "--extra",
        dest="extra",
        type=int,
        help="Number of nested iterations",
        default=EXTRA_DEFAULT,
    )
    parser.add_argument(
        "-r",
        "--reverse",
        dest="reverse",
        action="store_true",
        help="Reverses compression iterations (lower to higher)",
    )

    parser.add_argument(
        "-c",
        "--color",
        dest="color",
        type=float,
        help="Color enhancement",
        default=COLOR_DEFAULT,
    )

    parser.add_argument(
        "-o",
        "--output",
        dest="output_path",
        type=pathlib.Path,
        help="Output image filename",
        default=OUTPUT_DEFAULT,
    )

    parser.add_argument(
        "-p",
        "--preprocess",
        dest="preprocess",
        action="store_true",
        help="Adds color enhancement BEFORE compression",
    )

    return parser


def validate_input_path(namespace: argparse.Namespace) -> None:
    if not namespace.input_path.exists():
        msg = f"Input path does not exist: {namespace.input_path}"
        raise TypeError(msg)

    if not namespace.input_path.is_file():
        msg = "Input path should be a file."
        raise TypeError(msg)


def validate_iterations(namespace: argparse.Namespace) -> None:
    if namespace.iterations <= 0:
        msg = f"Iterations must be greater or equal to 1: {namespace.iterations}"
        raise TypeError(msg)


def validate_extra(namespace: argparse.Namespace) -> None:
    if namespace.extra <= 0:
        msg = f"Extra must be greater or equal to 1: {namespace.extra}"
        raise TypeError(msg)


def validate_color(namespace: argparse.Namespace) -> None:
    if namespace.color < 0.0:
        msg = f"Color enhancement must be greater or equal to 0.0: {namespace.color}"
        raise TypeError(msg)


def main() -> None:
    parser = get_argparser()

    namespace = parser.parse_args(sys.argv[1:])

    validate_input_path(namespace)
    validate_iterations(namespace)
    validate_extra(namespace)
    validate_color(namespace)

    run(
        input_path=namespace.input_path,
        output_path=namespace.output_path,
        iterations=namespace.iterations,
        extra=namespace.extra,
        color=namespace.color,
        reverse=namespace.reverse,
        preprocess=namespace.preprocess,
    )

    print("Done!")  # noqa: T201
