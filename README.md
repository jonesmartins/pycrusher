# pyCrusher 0.3.8

**Crusher (Wikipedia):**
>Crushers may be used to reduce the size, or change the form, of waste materials so they can be more easily disposed of or recycled..."

Much like an actual crusher, *pyCrusher* copies your precious little images and turns them into absolute trash (for fun!)

## Installation
Install this program through pip:

Linux/MacOS:
```sh
sudo pip install -U pycrusher
```

Windows:
```sh
py(or python) -m pip install -U pycrusher
```

Or download this package and manually run:
```sh
sudo python setup.py install
```

## Usage:
Type in the command line:
```sh
~/path/to/somewhere $ pycrusher <image_file> <flags and parameters>
```
Windows:
```sh
C:\path\to\somewhere > py -m pycrusher <image_file> <flags and parameters>
or
C:\path\to\somewhere > pycrusher <image_file> <flags and parameters>
```

As default, the program saves your output in a special directory called 'compressions' located at `path/to/somewhere`, so if you use *pyCrusher* multiple times in `path/to/somewhere`, you can check your compressed images without mixing it up between your other files.
Every time you save a new file in 'compressions', your output file will be saved with your input name followed by the compression settings. You can still use the -o/--output flag and name it however you want.

Default name: `compression/<image-name>_i<iterations>e<extra><r><p><c>[colors].<extension>`

### Options:

**-h, --help**

Display the help information.

**-i, --iterations ITERATIONS**

How many times you want your image to be compressed. Default: 50

**-e, --extra EXTRA**

How many times you want ITERATIONS to happen. Usually enforces the effect of ITERATIONS. Default: 1

**-c, --colors [COLOR, ...]**

Different saturation values you want the image to be post-processed with. They are read in order. Default: [1.0]

**-o, --output OUTFILENAME**

Name of output, which will also be saved in 'compressions'.

**-r, --reverse**

Flag that means file will compress image from worst quality to best, creating a 'blockier' image.

**-p, --preprocess**

Flag that applies color changes from -c, --colors before compressing, might create interesting effects.

## Examples:
Our image: crusher.png

![crusher](https://cloud.githubusercontent.com/assets/15959626/22045694/f78ef41c-dd02-11e6-9594-cd6b00e02884.png)


```sh
$ pycrusher crusher.png
```
**output**:  compressions/crusher_i50e1.png
![compressed_crusher0](https://cloud.githubusercontent.com/assets/15959626/22045698/fa458d24-dd02-11e6-8265-fdf3b902cded.jpg)
#
```sh
$ pycrusher crusher.png -i 10
```
**output**: compressions/crusher_i10e1.png
![compressed_crusher6](https://cloud.githubusercontent.com/assets/15959626/22045854/0fc4f148-dd04-11e6-9e4d-fd60504fc2d5.jpg)
#
```sh
$ pycrusher crusher.png -i 10 -e 5
```
**output**:  compressions/crusher_i10e5.png
![compressed_crusher1](https://cloud.githubusercontent.com/assets/15959626/22045717/1883c198-dd03-11e6-9e76-4a6cb20c0413.jpg)
#
```sh
$ pycrusher crusher.png -i 20 -c 4
```
**output**: compressions/crusher_i20e1c[4.0].png
![compressed_crusher7](https://cloud.githubusercontent.com/assets/15959626/22045906/63ef3a76-dd04-11e6-9ed0-4080a7c92ab9.jpg)
#
```sh
$ pycrusher crusher.png -i 20 -c 4 -r
```
**output**: compressions/crusher_i20e1rc[4.0].png
![compressed_crusher5](https://cloud.githubusercontent.com/assets/15959626/22492147/6bc72270-e80f-11e6-8e64-fa678fa03b0a.png)
#
```sh
$ pycrusher crusher.png -i 20 -c 4 0
```
**output**:  compressions/crusher_i20e1c[4.0,0.0].png
![compressed_crusher5](https://cloud.githubusercontent.com/assets/15959626/22045830/d62aae5a-dd03-11e6-8efd-a3fb90b42f0b.jpg)
#
```sh
$ pycrusher crusher.png -i 20 -c 4 0 -p
```
**output**: compressions/crusher_i20e1pc[4.0,0.0].png
![compressed_crusher1](https://cloud.githubusercontent.com/assets/15959626/22492096/1640df30-e80f-11e6-94b5-3adedc6771b4.png)
