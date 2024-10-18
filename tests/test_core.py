from __future__ import annotations

import pathlib
import tempfile
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from collections.abc import Iterable

import hypothesis
import pytest
from hypothesis import strategies as st

from pycrusher.core import (
    compress,
    generate_quality_sequence,
)

SMALL_TEST_IMAGES = pathlib.Path("tests/images/small")


class TestGetQualities:
    T = TypeVar("T")

    @staticmethod
    def pairwise(iterable: Iterable[T]) -> tuple[T, T]:
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
    @pytest.mark.parametrize("input_path", SMALL_TEST_IMAGES.iterdir())
    @hypothesis.given(
        iterations=st.integers(min_value=1, max_value=2),
        extra=st.integers(min_value=1, max_value=2),
        reverse=st.booleans(),
    )
    def test_compress_works_at_all(
        self,
        input_path: pathlib.Path,
        iterations: int,
        extra: int,
        reverse: bool,
    ) -> None:
        with tempfile.NamedTemporaryFile(suffix=".jpg") as tmp:
            tmp.write(input_path.read_bytes())

            output_filename = pathlib.Path(tmp.name)
            qualities = generate_quality_sequence(iterations, reverse)

            compress(
                output_filename,
                extra * qualities,
            )

    @hypothesis.settings(deadline=None)
    @pytest.mark.parametrize("input_path", SMALL_TEST_IMAGES.iterdir())
    @hypothesis.given(
        iterations=st.integers(min_value=1, max_value=5),
        extra=st.integers(min_value=1, max_value=3),
        reverse=st.booleans(),
    )
    def test_compress(
        self,
        input_path: pathlib.Path,
        iterations: int,
        extra: int,
        reverse: bool,
    ) -> None:
        with tempfile.NamedTemporaryFile(suffix=".jpg") as tmp:
            tmp.write(input_path.read_bytes())

            output_filename = pathlib.Path(tmp.name)
            qualities = generate_quality_sequence(iterations, reverse)

            compress(
                output_filename,
                extra * qualities,
            )
