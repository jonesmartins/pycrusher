#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function

import argparse
import os
import re
import sys
import tqdm

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


def make_dir(dir_name):
    """Makes sure target directory doesn't exist, or that the
    command wasn't called from inside said directory.
    Args:
        dir_name(str): Name of directory where all compressed
            images will be stored. Usually called 'compressed'
    Returns:
        dir_name(str): Same as above.
    """
    if not os.path.isdir(dir_name):  # dir_name doesn't exist
        if dir_name in os.getcwd():  # but already inside dir_name
            return ''                # doesn't add dir_name to path
        os.mkdir(dir_name)           # else, creates it 
    return dir_name                  # returns name, so adds to path


def check_filenames(input_name, output_name):
    """This function prepares the file to be saved in another
    format, so it removes its format and inserts 'compressed_'
    before the actual name to avoid collisions. If user inserted
    a correct output_name, nothing happens to it.
    Args:
        input_name(str): Name of input file
        output_name(str): Name of output file (optional)
    Returns:
        Returns output(str) and its format(str) in a list.
    Raises:
        ValueError: File format not in acceptable set
    """ 
    if not output_name:
        output_name = os.path.basename(input_name)
        '''
        if 'compressed_' in input_name:
            output_name = os.path.basename(input_name)
        else:
            output_name = 'compressed_{}'.format(os.path.basename(input_name))
        '''
    acceptable = set(['.bmp',  '.jpg', '.pbm', '.pgm',
                      '.png', '.ppm', '.rgb', '.webp'])
    
    input_path = os.path.splitext(os.path.basename(input_name))
    output_path = os.path.splitext(os.path.basename(output_name))
    
    if input_path[1] not in acceptable:
        raise ValueError('Input format {} not acceptable!'.format(input_path[1]))

    if not output_path[0] or output_path[1] not in acceptable:
        # User gave partial output(no name or no format) or gave wrong format
        print(output_path)
        raise ValueError('Output not acceptable!')
    
    return os.path.splitext(os.path.basename(output_name))
    

# I will leave this function just in case, but has no use for now
def generate_version_number(typeless_output, file_format, dir_name=''):
    """Tries to open dir_name, if it can't, you're inside it.
    Then it tries to see the last file with similar name and generates
    a new version.
    Args:
        typeless_output(str): Typeless name of output, given by check_filenames
        file_format(str): Needs format to look for different name        
        dir_name(str)[Optional]: Name of directory to store compressed images
    Returns:
        If file exists, returns maximum version found + 1, else it returns 1
    Raises:
        ValueError: past_versions is empty
    """
    try:
        files = os.listdir(dir_name)
    except OSError:
        files = os.listdir(os.getcwd())
        
    filenames = ' '.join(files)
    try:
        file_template = re.compile(r'{}\_(\d*){}'.format(typeless_output,
                                                         file_format))
        past_versions = re.findall(file_template, filenames)
        # Gets maximum version available
        latest = max([int(v) for v in past_versions])
    except ValueError:
        # Couldn't find any past versions
        latest = 0
        
    return latest + 1


def get_final_output_name(input_name, output_name='',
                          iterations=50, extra=1,
                          colors=1.0, reverse=False,
                          preprocess=False, dir_name=''):
    """Gets all files related to the output and runs them all together.
    Args:
        input_name(str): Input given by parse_args.
        output_name(str)[Optional]: Output given by parse_args.
        iterations(int)[Optional]: How many times to iterate compression
        extra(int)[Optional]: How much to enforce compression
        colors(List[float])[Optional]: Adds 'c' and list of colors to final name
        reverse(bool)[Optional]: Adds 'r' to final name to indicate use
        preprocess(bool)[Optional]: Adds 'p' to final name to indicate use
        dir_name(str)[Optional]: Name of directory to store compressed images
    Returns:
        String representing the final file name, with some info about its
        configuration.
    """
    typeless_output, file_format = check_filenames(input_name,
                                                   output_name)
    if not output_name:
        typeless_output = '{}_i{}e{}'.format(typeless_output,
                                             iterations,
                                             extra)
        if reverse:
            typeless_output += 'r'
        if preprocess:
            typeless_output += 'p'
        if colors != [1.0] or colors != 1.0:
            typeless_output += 'c{}'.format(str(colors).replace(' ', ''))
    return os.path.join(dir_name, '{}{}'.format(typeless_output, file_format))


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


def main():
    cmd = read_argv(sys.argv[1:])
    cmd_dict = check_cmd(cmd)  # checks Namespace. Can also be dict
    dir_name = make_dir('compressions')
    lossy_compress(cmd_dict['file'], cmd_dict['output'],
                   cmd_dict['iterations'], cmd_dict['extra'],
                   cmd_dict['colors'], cmd_dict['reverse'],
                   cmd_dict['preprocess'], dir_name)
    print("Done!")

    
if __name__ == '__main__':
    main()

