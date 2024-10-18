# pyCrusher

[![pyCrusher version](https://img.shields.io/pypi/v/pycrusher.svg)](https://pypi.org/project/pycrusher)
[![PyPI downloads](https://static.pepy.tech/badge/pycrusher)](https://pepy.tech/project/pycrusher)
![Accepted Python versions](https://img.shields.io/pypi/pyversions/pycrusher.svg)

**Crusher (Wikipedia):**
>Crushers may be used to reduce the size, or change the form, of waste materials so they can be more easily disposed of or recycled..."

Much like an actual crusher, *pyCrusher* copies your precious little images and turns them into absolute trash (for fun!)

## Install instructions

### [Pipx](https://pipx.pypa.io/stable/)

```bash
pipx install pycrusher
```

### Uv

```bash
uv tool install pycrusher
```

### Pip

```bash
pip install pycrusher
```

### Download manually (Linux/MacOS)

```bash
git clone https://github.com/jonesmartins/pycrusher
cd pycrusher
python setup.py install
```

## Usage

Type in the command line:

```bash
pycrusher <image_file> <flags and parameters>
```

As default, the program saves your output in a special directory called 'compressions' located at `path/to/somewhere`, so if you use *pyCrusher* multiple times in `path/to/somewhere`, you can check your compressed images without mixing it up between your other files.
Every time you save a new file in 'compressions', your output file will be saved with your input name followed by the compression settings. You can still use the -o/--output flag and name it however you want.

Default name: `compression/<image-name>_i<iterations>e<extra><r><p><c>[colors].<extension>`

### Options

```txt
usage: pycrusher [-h] [-i ITERATIONS] [-e EXTRA] [-c [COLORS ...]] [-o OUTPUT] [-r] [-p] file

positional arguments:
  file                  Name of image to compress

options:
  -h, --help            show this help message and exit
  -i ITERATIONS, --iterations ITERATIONS
                        Number of compression iterations
  -e EXTRA, --extra EXTRA
                        Number of nested iterations
  -c [COLORS ...], --colors [COLORS ...]
                        Color changes
  -o OUTPUT, --output OUTPUT
                        Name of output file.
  -r, --reverse         Reverses compression iterations.
  -p, --preprocess      Adds color enhancement BEFORE compression.
```

## Examples

**Original image:** crusher.png

![crusher](https://cloud.githubusercontent.com/assets/15959626/22045694/f78ef41c-dd02-11e6-9594-cd6b00e02884.png)

---

```bash
pycrusher crusher.png
```

**Default output filename:**   compressions/crusher_i50e1.png

![compressed_crusher0](https://cloud.githubusercontent.com/assets/15959626/22045698/fa458d24-dd02-11e6-8265-fdf3b902cded.jpg)

---

```bash
pycrusher crusher.png -i 10
```

**Default output filename:**  compressions/crusher_i10e1.png

![compressed_crusher6](https://cloud.githubusercontent.com/assets/15959626/22045854/0fc4f148-dd04-11e6-9e4d-fd60504fc2d5.jpg)

---

```bash
pycrusher crusher.png -i 10 -e 5
```

**Default output filename:**   compressions/crusher_i10e5.png

![compressed_crusher1](https://cloud.githubusercontent.com/assets/15959626/22045717/1883c198-dd03-11e6-9e76-4a6cb20c0413.jpg)

---

```bash
pycrusher crusher.png -i 20 -c 4
```

**Default output filename:**  compressions/crusher_i20e1c[4.0].png

![compressed_crusher7](https://cloud.githubusercontent.com/assets/15959626/22045906/63ef3a76-dd04-11e6-9ed0-4080a7c92ab9.jpg)

---

```bash
pycrusher crusher.png -i 20 -c 4 -r
```

**Default output filename:** compressions/crusher_i20e1rc[4.0].png

![compressed_crusher5](https://cloud.githubusercontent.com/assets/15959626/22492147/6bc72270-e80f-11e6-8e64-fa678fa03b0a.png)

---

```bash
pycrusher crusher.png -i 20 -c 4 0
```

**Default output filename:**  compressions/crusher_i20e1c[4.0,0.0].png

![compressed_crusher5](https://cloud.githubusercontent.com/assets/15959626/22045830/d62aae5a-dd03-11e6-8efd-a3fb90b42f0b.jpg)

---

```bash
pycrusher crusher.png -i 20 -c 4 0 -p
```

**Default output filename:**  compressions/crusher_i20e1pc[4.0,0.0].png

![compressed_crusher1](https://cloud.githubusercontent.com/assets/15959626/22492096/1640df30-e80f-11e6-94b5-3adedc6771b4.png)

## License

Apache License 2.0
