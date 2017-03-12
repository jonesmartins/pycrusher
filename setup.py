from setuptools import setup

__version__ = "0.3.8"

version_url = 'https://github.com/jonesmartins/pycrusher/tarball/'\
             + __version__
setup(
    name='pycrusher',
    version=__version__,
    url='https://github.com/jonesmartins/pycrusher',
    download_url=version_url, 
    license='MIT',
    author='Jones Martins',
    author_email='jonesmvc@hotmail.com',
    description='Generate lossy image compressions for fun!',
    keywords=['lossy', 'compression', 'compress', 'jpeg'], 
    install_requires=['Pillow', 'argparse', 'tqdm'], 
    packages=['pycrusher'],
    entry_points={'console_scripts': ['pycrusher=pycrusher._main:main']},    
    )
