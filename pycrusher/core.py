from __future__ import absolute_import
from __future__ import print_function
from __future__ import annotations

import os
import sys
import tqdm

from .name_generator import get_final_output_name
from PIL import Image, ImageFile, ImageEnhance


def prepare_compression(input_name: str, output_name: str, dir_name: str = "") -> None:
    """First thing done with the file. Opens and saves it in dir_name
    with the final name.
    Args:
        input_name(str): Input given by parse_args.
        output_name(str): String representing the final file name,
                                with version and format.
        dir_name(str)[Optional]:
    Raises:
        OSError: Input_name doesn't exist.
    """
    try:
        files = os.listdir(dir_name)
    except OSError:
        files = os.listdir(os.getcwd())
    try:
        with Image.open(input_name) as img:
            split_name = os.path.split(output_name)[1]
            if split_name in files:
                print("{} already exists! ".format(split_name))
                saving = input("Do you want to overwrite it?(y/n) ")
                if saving.lower() == "n":
                    sys.exit("Exiting...")
            img.save(output_name)
    except OSError:
        sys.exit("{} doesn't exist.".format(input_name))


def compress(final_output, qualities: list[int]) -> None:
    """Compresses file in a quality calculated real time.
    This quality is based on percentage, where 'iterations' is the total.
    Returns the last_quality, so the file can be saved for the last
    time without increasing file size.
    Args:
        final_output(str): String representing the final file name,
                                with version and format.
        iterations(int)[Optional]: How many times to iterate compression
        extra(int)[Optional]: How much to enforce compression
        reverse_bool(bool)[Optional]: If True, goes from zero to 'iterations'.
    Raises:
        PermissionError: I don't really know why it happens.
    """
    print(f"compressing with qualities {qualities}")
    for quality in tqdm.tqdm(qualities):
        while True:
            try:
                with Image.open(final_output) as img:
                    img.convert("RGB")
                    img.save(final_output, format="JPEG", quality=quality)
                break
            except PermissionError:
                pass


def change_colors(final_output: str, color: float, quality: int) -> None:
    """Changes color of image multiple times and saves in the
    last compression quality.
    Args:
        final_output(str): String representing the final file name,
                                with version and format.
        colors(float): Colors to change.
        quality(int): Last quality of compression
    Returns:
        Nothing.
    Raises:
        PermissionError: I don't really know why it happens,
                             I just try until it works.
    """
    while True:
        try:
            with Image.open(final_output) as img:
                converter = ImageEnhance.Color(img)
                img = converter.enhance(color)
                img.save(final_output, quality=quality)
            break
        except PermissionError:
            pass


def get_qualities(iterations: int, extra: int, reverse: bool) -> list[int]:
    qualities = [int(100 * (float(i) / float(iterations))) for i in range(iterations)]
    if not reverse:
        qualities = [100 - q for q in qualities]
    return qualities * extra


def lossy_compress(
    file: str,
    output: str = "",
    iterations: int = 50,
    extra: int = 1,
    color: float = 1.0,
    reverse: bool = False,
    preprocess: bool = False,
    dir_name: str = "",
) -> None:
    ImageFile.MAXBLOCK = 2**22
    final_output = get_final_output_name(
        file, output, iterations, extra, color, reverse, preprocess, dir_name
    )
    prepare_compression(file, final_output, dir_name)

    qualities = get_qualities(iterations, extra, reverse)
    print("Qualities:", qualities)
    if not qualities:
        return

    if preprocess:
        change_colors(final_output, color, quality=qualities[0])
        compress(final_output, qualities)
    else:
        compress(final_output, qualities)
        change_colors(final_output, color, quality=qualities[-1])
