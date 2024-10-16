from __future__ import annotations
import os

import pathlib
import tempfile

import hypothesis
import pytest
from hypothesis import strategies as st
from PIL import Image

from pycrusher.core import compress, get_qualities
from pycrusher.name_generator import get_final_output_name

SMALL_TEST_IMAGES = pathlib.Path("tests/images/small")


@hypothesis.given(
    iterations=st.integers(min_value=0, max_value=10),
    extra=st.integers(min_value=0, max_value=10),
    reverse=st.booleans(),
)
def test_get_qualities(
    iterations: int,
    extra: int,
    reverse: bool,
):
    qualities = get_qualities(iterations, extra, reverse)
    assert len(qualities) == iterations * extra


@pytest.mark.parametrize("input_path", SMALL_TEST_IMAGES.iterdir())
@hypothesis.given(
    iterations=st.integers(min_value=0, max_value=2),
    extra=st.integers(min_value=0, max_value=2),
    reverse=st.booleans(),
)
def test_compress_works_at_all(
    input_path: pathlib.Path,
    iterations: int,
    extra: int,
    reverse: bool,
):
    with tempfile.NamedTemporaryFile(suffix=".jpg") as tmp:
        tmp.write(input_path.read_bytes())

        output_filename = pathlib.Path(tmp.name)
        print(output_filename)
        qualities = get_qualities(iterations, extra, reverse)

        compress(
            output_filename,
            qualities,
        )


@hypothesis.settings(deadline=None)
@hypothesis.given(
    iterations=st.integers(min_value=1, max_value=3),
    extra=st.integers(min_value=1, max_value=3),
    reverse=st.booleans(),
    preprocess=st.booleans(),
    color=st.floats(min_value=0.0),
)
def test_pycrusher_works_at_all(
    iterations: int,
    extra: int,
    reverse: bool,
    preprocess: bool,
    color: float,
):
    input_filename = "tests/images/small/esfr_chart_217p.jpg"
    extra_arg = ""
    if extra > 1:
        extra_arg = f"-e {extra}"

    reverse_arg = ""
    if reverse:
        reverse_arg = "--reverse"
    preprocess_arg = ""
    if preprocess:
        preprocess_arg = "--preprocess"

    import subprocess

    output_filename = get_final_output_name(
        input_filename,
        output_name="",
        iterations=iterations,
        extra=extra,
        color=color,
        reverse=reverse,
        preprocess=preprocess,
        dir_name="compressions",
    )

    return_code = subprocess.call(
        f"uv run python3 -m pycrusher {input_filename} -i {iterations} {extra_arg} {reverse_arg} {preprocess_arg} --color {color}".split()
    )
    assert return_code == 0
    assert os.path.exists(output_filename)
