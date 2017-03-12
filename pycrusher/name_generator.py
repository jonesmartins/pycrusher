#!/usr/bin/env python
import os


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
