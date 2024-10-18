from __future__ import annotations

import io
import pathlib
from typing import TYPE_CHECKING, Generator, TypeVar

if TYPE_CHECKING:
    from collections.abc import Iterable

import hypothesis
import pytest
from hypothesis import strategies as st

from pycrusher.core import compress, generate_quality_sequence
from tests.utils import SMALL_TEST_IMAGES_DIRECTORY, same_pixels_in_image_files


class TestGetQualities:
    T = TypeVar("T")

    # itertools.pairwise was added in python 3.10
    @staticmethod
    def pairwise(iterable: Iterable[T]) -> Generator[tuple[T | None, T], T, None]:
        iterator = iter(iterable)
        a = next(iterator, None)
        for b in iterator:
            yield a, b
            a = b

    @hypothesis.given(
        iterations=st.integers(min_value=1, max_value=10),
        reverse=st.booleans(),
    )
    def test_get_qualities(
        self,
        iterations: int,
        reverse: bool,
    ) -> None:
        qualities = generate_quality_sequence(iterations, reverse=reverse)
        assert len(qualities) == iterations

        if len(qualities) >= 1:
            if reverse:
                assert qualities[0] == 0
            else:
                assert qualities[0] == 100

        if len(qualities) > 1:
            delta = 100 // len(qualities)
            for a, b in self.pairwise(qualities):
                if reverse:
                    assert a < b
                else:
                    assert a > b
                assert abs(a - b) == delta


class TestGetDefaultOutputName:
    def test_get_default_output_name(self) -> None:
        pass


class TestChangeColors:
    def test_change_color(self) -> None:
        pass


class TestCompress:
    @hypothesis.settings(deadline=None)
    @pytest.mark.parametrize("input_path", SMALL_TEST_IMAGES_DIRECTORY.iterdir())
    @hypothesis.given(
        iterations=st.integers(min_value=1, max_value=2),
        extra=st.integers(min_value=1, max_value=2),
        reverse=st.booleans(),
    )
    def test_compress_raises_no_exceptions(
        self,
        input_path: pathlib.Path,
        iterations: int,
        extra: int,
        reverse: bool,
    ) -> None:
        buf = io.BytesIO(input_path.read_bytes())

        qualities = extra * generate_quality_sequence(iterations, reverse)

        compress(
            buf,
            qualities,
        )

    @hypothesis.settings(deadline=None)
    @pytest.mark.parametrize("input_path", SMALL_TEST_IMAGES_DIRECTORY.iterdir())
    @hypothesis.given(
        iterations=st.integers(min_value=2, max_value=5),
        extra=st.integers(min_value=2, max_value=3),
        reverse=st.booleans(),
    )
    def test_compress(
        self,
        input_path: pathlib.Path,
        iterations: int,
        extra: int,
        reverse: bool,
    ) -> None:
        buf = io.BytesIO(input_path.read_bytes())

        qualities = extra * generate_quality_sequence(iterations, reverse)

        compress(
            buf,
            qualities,
        )

        assert not same_pixels_in_image_files(input_path, buf)
