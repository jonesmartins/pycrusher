from __future__ import absolute_import
from __future__ import annotations

import sys
import argparse

from .name_generator import make_dir
from .core import lossy_compress


def get_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pycrusher")
    parser.add_argument("file", type=str, help="Name of image to compress")
    parser.add_argument(
        "-i",
        "--iterations",
        dest="iterations",
        type=int,
        help="Number of compression iterations",
        default=50,
    )
    parser.add_argument(
        "-e",
        "--extra",
        dest="extra",
        type=int,
        help="Number of nested iterations",
        default=1,
    )
    parser.add_argument(
        "-c",
        "--color",
        dest="color",
        type=float,
        help="Color change",
        default=1.0,
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        type=str,
        help="Name of output file.",
    )
    parser.add_argument(
        "-r",
        "--reverse",
        dest="reverse",
        action="store_true",
        help="Reverses compression iterations.",
    )
    parser.add_argument(
        "-p",
        "--preprocess",
        dest="preprocess",
        action="store_true",
        help="Adds color enhancement BEFORE compression.",
    )

    return parser


def main() -> None:
    parser = get_argparser()
    dir_name = make_dir("compressions")
    namespace = parser.parse_args(sys.argv[1:])
    lossy_compress(
        namespace.file,
        namespace.output,
        namespace.iterations,
        namespace.extra,
        namespace.color,
        namespace.reverse,
        namespace.preprocess,
        dir_name,
    )
    print("Done!")
