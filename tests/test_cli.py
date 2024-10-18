from __future__ import annotations

import argparse
import pathlib

import hypothesis
import pytest
from hypothesis import strategies as st
from importlib_metadata import version

from pycrusher.cli import (
    COLOR_DEFAULT,
    EXTRA_DEFAULT,
    ITERATIONS_DEFAULT,
    OUTPUT_DEFAULT,
    PROGRAM,
    get_argparser,
    validate_color,
    validate_extra,
    validate_input_path,
    validate_iterations,
)
from tests.utils import SMALL_TEST_IMAGES_DIRECTORY


class TestParseArgs:
    def test_input_path(self, capsys: pytest.CaptureFixture[str]) -> None:
        # Input_path is required
        # Parsed as path
        parser = get_argparser()
        namespace = parser.parse_args(["placeholder_path"])
        assert namespace.input_path == pathlib.Path("placeholder_path")
        with pytest.raises(SystemExit):
            # Input_path is the only required argument
            parser.parse_args([])

    @pytest.mark.parametrize("arg", ["-i", "--iterations"])
    @hypothesis.given(iterations=st.integers())
    def test_iterations(self, arg: str, iterations: int) -> None:
        # Extra is optional
        # Extra is integer
        # -e, or --extra
        # If missing, default is 1
        parser = get_argparser()

        namespace = parser.parse_args(["placeholder_path", arg, str(iterations)])
        assert namespace.iterations == iterations

        namespace = parser.parse_args(["placeholder_path"])
        assert namespace.iterations == ITERATIONS_DEFAULT

    @pytest.mark.parametrize("arg", ["-e", "--extra"])
    @hypothesis.given(extra=st.integers())
    def test_extra(self, arg: str, extra: int) -> None:
        # Extra is optional
        # Extra is integer
        # -e, or --extra
        # If missing, default is 1
        parser = get_argparser()

        namespace = parser.parse_args(["placeholder_path", arg, str(extra)])
        assert namespace.extra == extra

        namespace = parser.parse_args(["placeholder_path"])
        assert namespace.extra == EXTRA_DEFAULT

    @pytest.mark.parametrize("arg", ["-c", "--color"])
    @hypothesis.given(color=st.floats(min_value=0.0))
    def test_color(self, arg: str, color: float) -> None:
        # Color is optional
        # Color is float
        # -c, or --color
        # If missing, default is 1.0
        parser = get_argparser()

        namespace = parser.parse_args(["placeholder_path", arg, str(color)])
        assert namespace.color == color

        namespace = parser.parse_args(["placeholder_path"])
        assert namespace.color == COLOR_DEFAULT

    @pytest.mark.parametrize("arg", ["-o", "--output"])
    def test_output_path(self, arg: str) -> None:
        # Output is optional
        # Output is Path
        # -o or --output
        # If missing, default is None
        output_path = pathlib.Path("foo")
        parser = get_argparser()

        namespace = parser.parse_args(["placeholder_path", arg, str(output_path)])
        assert namespace.output_path == output_path

        namespace = parser.parse_args(["placeholder_path"])
        assert namespace.output_path == OUTPUT_DEFAULT

    @pytest.mark.parametrize("arg", ["-r", "--reverse"])
    def test_reverse(self, arg: str) -> None:
        # Reverse is optional
        # Reverse is bool
        # -r or --reverse
        # If missing, False. Else, true
        parser = get_argparser()

        namespace = parser.parse_args(["placeholder_path", arg])
        assert namespace.reverse

        namespace = parser.parse_args(["placeholder_path"])
        assert not namespace.reverse

    @pytest.mark.parametrize("arg", ["-p", "--preprocess"])
    def test_preprocess(self, arg: str) -> None:
        # Preprocess is optional
        # Preprocess is bool
        # -p or --preprocess
        # If missing, false. Else, true
        parser = get_argparser()

        namespace = parser.parse_args(["placeholder_path", arg])
        assert namespace.preprocess

        namespace = parser.parse_args(["placeholder_path"])
        assert not namespace.preprocess

    @hypothesis.given(st.permutations(["-i 1", "-e 1", "-c 1", "-r", "-p", "-o out"]))
    def test_input_path_in_edges_of_args(self, permutated_args: list[str]) -> None:
        parser = get_argparser()

        joined_args1 = " ".join(["placeholder_path", *permutated_args])
        joined_args2 = " ".join([*permutated_args, "placeholder_path"])

        namespace1 = parser.parse_args(joined_args1.split())
        namespace2 = parser.parse_args(joined_args2.split())

        expected_namespace = argparse.Namespace(
            input_path=pathlib.Path("placeholder_path"),
            iterations=1,
            extra=1,
            color=1.0,
            reverse=True,
            preprocess=True,
            output_path=pathlib.Path("out"),
        )
        assert namespace1 == expected_namespace
        assert namespace2 == expected_namespace

    def test_cli_help_exits_with_retcode_zero(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """
        Test that '-h' and '--help' behave the same:
        They raise SystemExit(0) and output the same message.
        """
        parser = get_argparser()

        with pytest.raises(SystemExit) as exc_info:
            parser.parse_args(["-h"])
        assert exc_info.value.args[0] == 0
        capture1 = capsys.readouterr()

        with pytest.raises(SystemExit) as exc_info:
            parser.parse_args(["--help"])
        assert exc_info.value.args[0] == 0
        capture2 = capsys.readouterr()

        assert capture1.out == capture2.out

    def test_cli_version_exits_with_retcode_zero(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """
        Test that '-v' and '--version' behave the same:
        Both raise SystemExit(0) and output the same message.
        """
        argparser = get_argparser()
        with pytest.raises(SystemExit) as exc_info:
            argparser.parse_args(["-v"])
        assert exc_info.value.args[0] == 0
        capture1 = capsys.readouterr()

        with pytest.raises(SystemExit) as exc_info:
            argparser.parse_args(["--version"])
        assert exc_info.value.args[0] == 0
        capture2 = capsys.readouterr()

        assert capture1.out == capture2.out

        assert capture1.out == f"{PROGRAM} {version(PROGRAM)}\n"


class TestValidateNamespace:
    @pytest.mark.parametrize("input_path", SMALL_TEST_IMAGES_DIRECTORY.iterdir())
    def test_valid_input_path(self, input_path: pathlib.Path) -> None:
        validate_input_path(argparse.Namespace(input_path=input_path))

    @hypothesis.given(st.uuids().map(lambda u: pathlib.Path(str(u))))
    def test_invalid_input_path_does_not_exist(self, input_path: pathlib.Path) -> None:
        with pytest.raises(
            TypeError,
            match="Input path does not exist:",
        ):
            validate_input_path(argparse.Namespace(input_path=input_path))

    def test_invalid_input_path_is_not_directory(self, tmpdir: pathlib.Path) -> None:
        with pytest.raises(
            TypeError,
            match="Input path should be a file.",
        ):
            validate_input_path(argparse.Namespace(input_path=pathlib.Path(tmpdir)))

    @hypothesis.given(iterations=st.integers(max_value=0))
    def test_invalid_iterations(self, iterations: int) -> None:
        with pytest.raises(
            TypeError,
            match="Iterations must be greater or equal to 1:",
        ):
            validate_iterations(argparse.Namespace(iterations=iterations))

    @hypothesis.given(iterations=st.integers(min_value=1))
    def test_valid_iterations(self, iterations: int) -> None:
        validate_iterations(argparse.Namespace(iterations=iterations))

    @hypothesis.given(extra=st.integers(max_value=0))
    def test_invalid_extra(self, extra: int) -> None:
        with pytest.raises(
            TypeError,
            match="Extra must be greater or equal to 1:",
        ):
            validate_extra(argparse.Namespace(extra=extra))

    @hypothesis.given(extra=st.integers(min_value=1))
    def test_valid_extra(self, extra: int) -> None:
        validate_extra(argparse.Namespace(extra=extra))

    @hypothesis.given(color=st.floats(max_value=-1e5))
    def test_invalid_color(self, color: float) -> None:
        with pytest.raises(
            TypeError,
            match="Color enhancement must be greater or equal to 0.0:",
        ):
            validate_color(argparse.Namespace(color=color))

    @hypothesis.given(color=st.floats(min_value=0))
    def test_valid_color(
        self,
        color: float,
    ) -> None:
        validate_color(argparse.Namespace(color=color))
