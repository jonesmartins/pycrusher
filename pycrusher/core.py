from __future__ import annotations

import io
import pathlib

import tqdm
from PIL import Image, ImageEnhance

COMPRESSIONS_DIRECTORY = pathlib.Path.cwd().joinpath("compressions")


def generate_default_output_name(
    input_path: pathlib.Path,
    *,
    iterations: int,
    extra: int,
    color: float,
    reverse: bool,
    preprocess: bool,
) -> str:
    """
    Generate default output name based on pycrusher parameters.

    Args:
        input_path (pathlib.Path): Input given by parse_args.
        iterations (int): How many times to iterate compression.
        extra (int): How much to enforce compression.
        color (float): Color saturation.
        reverse (bool): Reverse qualities.
        preprocess (bool): Preprocess color.

    Returns:
        Default output name based on pycrusher parameters.

    """
    output_suffixes = [f"i{iterations}", f"e{extra}"]
    if reverse:
        output_suffixes.append("rev")
    if preprocess:
        output_suffixes.append("pre")
    if color != 1.0:
        output_suffixes.append(f"c{color}")

    joined_suffixes = "_".join(output_suffixes)
    return f"{input_path.stem}_{joined_suffixes}.jpg"


def compress(
    image_buffer: io.BytesIO,
    qualities: list[int],
) -> None:
    """
    Save file repeatedly as JPEG for each quality in qualities.

    Args:
        image_buffer (io.BytesIO): Buffer containing image file.
        qualities (list[int]): List of JPEG qualities.

    """
    for quality in tqdm.tqdm(qualities):
        with Image.open(image_buffer) as img:
            img.load()

            image_buffer.seek(0)
            image_buffer.truncate()

            img.save(
                image_buffer,
                format="JPEG",
                quality=quality,
            )


def change_color(
    image_buffer: io.BytesIO,
    color: float,
    quality: int,
) -> None:
    """
    Change image saturation and save it with last compression quality.

    Args:
        image_buffer (io.BytesIO): Buffer containing image file.
        color (float): Color enhancement factor
        quality (int): JPEG quality

    """
    with Image.open(image_buffer) as img:
        converter = ImageEnhance.Color(img)
        enhanced_img = converter.enhance(color)

        image_buffer.seek(0)
        image_buffer.truncate()

        enhanced_img.save(
            image_buffer,
            format="JPEG",
            quality=quality,
        )


def generate_quality_sequence(
    iterations: int,
    reverse: bool,
) -> list[int]:
    """
    Generate JPEG quality sequence.

    Args:
        iterations (int): Number of iterations
        reverse (bool): Reverse list?

    Returns:
        List of JPEG qualities

    """
    # Quality sequence changed a bit, such that
    # qualities have uniform spacing.
    delta = 100 // iterations
    if reverse:
        qualities = [delta * i for i in range(iterations)]
    else:
        qualities = [100 - (delta * i) for i in range(iterations)]
    return qualities


def confirm(title: str, question: str) -> bool:
    """
    Confirm action.

    User is required to respond.

    Args:
        title (str): Top message, printed only once.
        question (str): Question user must respond.

    Returns:
        Confirm (True) or deny (False) question.

    """
    print(title)  # noqa: T201
    while True:
        confirm = input(f"{question} (y/n) ")
        if not confirm:
            continue
        if confirm.lower() in {"n", "no"}:
            return False
        if confirm.lower() in {"y", "yes"}:
            return True


def run(
    *,
    input_path: pathlib.Path,
    iterations: int,
    extra: int,
    color: float,
    reverse: bool,
    preprocess: bool,
    output_path: pathlib.Path | None,
) -> None:
    if output_path is None:
        default_output_name = generate_default_output_name(
            input_path,
            iterations=iterations,
            extra=extra,
            color=color,
            reverse=reverse,
            preprocess=preprocess,
        )
        output_path = COMPRESSIONS_DIRECTORY.joinpath(default_output_name)

    if output_path.exists():
        should_overwrite = confirm(
            title=f"File already exists: {output_path}",
            question="Do you want to overwrite it?",
        )
        if not should_overwrite:
            return

    qualities = extra * generate_quality_sequence(iterations, reverse)

    with io.BytesIO(input_path.read_bytes()) as image_buffer:
        if preprocess:
            change_color(image_buffer, color, quality=qualities[0])
            compress(image_buffer, qualities[1:])
        else:
            compress(image_buffer, qualities[:-1])
            change_color(image_buffer, color, quality=qualities[-1])

        output_path.write_bytes(image_buffer.getvalue())
