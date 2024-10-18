from __future__ import annotations

from pathlib import Path
from typing import IO

from PIL import Image

TEST_IMAGES_DIRECTORY = Path(__file__).parent.joinpath("images")
SMALL_TEST_IMAGES_DIRECTORY = TEST_IMAGES_DIRECTORY.joinpath("small")


def compare_images(
    i1: Image.Image,
    i2: Image.Image,
) -> bool:
    return list(i1.getdata()) == list(i2.getdata())


def open_and_compare_images(
    p1: str | bytes | Path | IO[bytes],
    p2: str | bytes | Path | IO[bytes],
) -> bool:
    with Image.open(p1) as i1, Image.open(p2) as i2:
        return compare_images(i1, i2)
