#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function

import argparse
import os
import sys
import tqdm

from .name_generator import get_final_output_name
from PIL import Image, ImageFile, ImageEnhance


def read_argv(argv):
    """Reads cmd arguments and returns a Namespace
    Args:
        argv(List of str): sys.argv commands
    Returns:
        Namespace of ArgumentParser
    """
    parser = argparse.ArgumentParser(prog='pycrusher')
    parser.add_argument('file',
                        type=str,
                        help='Name of image to compress')
    parser.add_argument('-i', '--iterations',
                        dest='iterations',
                        type=int,
                        help='Number of compression iterations',
                        default=50)
    parser.add_argument('-e', '--extra',
                        dest='extra',
                        type=int,
                        help='Number of nested iterations',
                        default=1)
    parser.add_argument('-c', '--colors',
                        dest='colors',
                        type=float,
                        nargs='*',
                        help='Color changes',
                        default=[1.0])
    parser.add_argument('-o', '--output',
                        dest='output',
                        type=str,
                        help='Name of output file.')
    parser.add_argument('-r', '--reverse',
                        dest='reverse',
                        action='store_true',
                        help='Reverses compression iterations.')
    parser.add_argument('-p', '--preprocess',
                        dest='preprocess',
                        action='store_true',
                        help='Adds color enhancement BEFORE compression.')

    return parser.parse_args(argv)


def check_cmd(cmd):
    """Makes sure program accepts a dictionary(for testing)
    or a Namespace class.
    Args:
        cmd(dict or Namespace class): commands and flags
    Returns:
        Dictionary of commands
    Raises:
        TypeError: In case cmd already is a dictionary
    """
    try:
        return vars(cmd)
    except TypeError:
        return cmd


def prepare_compression(input_name, output_name, dir_name=''):
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
                print('{} already exists! '.format(split_name))
                saving = input('Do you want to overwrite it?(y/n) ')
                if saving.lower() == 'n':
                    sys.exit('Exiting...')
            img.save(output_name)
    except OSError:
        sys.exit('{} doesn\'t exist.'.format(input_name))


def compress(final_output, iterations=50, extra=1, reverse_bool=False):
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
    Returns:
        curr_quality(int): Must return last quality saved so it doesn't
                           compromise image filesize at next step.
    Raises:
        PermissionError: I don't really know why it happens.
    """
    for ex in range(extra):            
        for it in tqdm.trange(iterations, desc='Loop {}'.format(ex+1)):
            curr_quality = int(100*(float(it)/float(iterations)))
            if not reverse_bool:
                curr_quality = 100 - curr_quality          
            while True:
                try:
                    with Image.open(final_output) as img:
                        img.convert("RGB")
                        img.save(final_output, format="JPEG",
                                 quality=curr_quality)
                    break
                except PermissionError:
                    pass
    try:
        return curr_quality  # Only if necessary
    except UnboundLocalError:
        print("Compression was not run.")


def change_colors(final_output, colors, quality):
    """Changes color of image multiple times and saves in the
    last compression quality.
    Args:
        final_output(str): String representing the final file name,
                                with version and format.
        colors(List[float]): List of presets of colors to change.
        quality(int): Last quality of compression
    Returns:
        Nothing.
    Raises:
        PermissionError: I don't really know why it happens,
                             I just try until it works.
    """    
    for color in colors:
        while True:
            try:
                with Image.open(final_output) as img:
                    converter = ImageEnhance.Color(img)                    
                    img = converter.enhance(color)
                    img.save(final_output, quality=quality)
                break
            except PermissionError:
                pass
    
    
def lossy_compress(file, output='', iterations=50, extra=1, colors=1.0,
                   reverse=False, preprocess=False, dir_name=''):
    ImageFile.MAXBLOCK = 2**22
    final_output = get_final_output_name(file, output, iterations, extra,
                                         colors, reverse, preprocess, dir_name)
    prepare_compression(file, final_output, dir_name)
    
    if preprocess:        
        if reverse:
            first_quality = 100
        else:
            first_quality = 0            
        change_colors(final_output, colors, first_quality)
        compress(final_output, iterations, extra, reverse)
    else:
        last_quality = compress(final_output, iterations, extra, reverse)
        change_colors(final_output, colors, last_quality)
