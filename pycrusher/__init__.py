from .name_generator import make_dir, check_filenames, get_final_output_name

from .core import prepare_compression, change_colors, compress, lossy_compress

from .cli import main

__all__ = [
    "make_dir",
    "check_filenames",
    "get_final_output_name",
    "lossy_compress",
    "prepare_compression",
    "change_colors",
    "compress",
    "lossy_compress",
    "main",
]
