import sys
import pycrusher.core as pycrusher

def main():
    cmd = pycrusher.read_argv(sys.argv[1:])
    cmd_dict = pycrusher.check_cmd(cmd)  # checks Namespace. Can also be dict
    dir_name = pycrusher.make_dir('compressions')
    lossy_compress(cmd_dict['file'], cmd_dict['output'],
                   cmd_dict['iterations'], cmd_dict['extra'],
                   cmd_dict['colors'], cmd_dict['reverse'],
                   cmd_dict['preprocess'], dir_name)
    print("Done!")

    
if __name__ == '__main__':
    main()
