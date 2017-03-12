from .name_generator import make_dir
from .name_generator import check_filenames
from .name_generator import get_final_output_name

from .core import read_argv
from .core import check_cmd
from .core import prepare_compression
from .core import change_colors
from .core import compress
from .core import lossy_compress

from ._main import main

__all__ = ['make_dir', 'check_filenames', 'get_final_output_name',
           'read_argv', 'check_cmd', 'lossy_compress', 'prepare_compression',
           'change_colors', 'compress', 'lossy_compress', 'main']
