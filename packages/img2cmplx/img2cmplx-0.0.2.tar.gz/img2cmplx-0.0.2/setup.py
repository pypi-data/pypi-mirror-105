from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Extract a simplicial complex from a raster'
LONG_DESCRIPTION = 'Perform some basic preprocessing on an image for TDA apps.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="img2cmplx",
        version=VERSION,
        author="David L. Millman",
        author_email="<dave@cs.unc.edu>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            'numpy',
            'scipy',
            'PIL',
            'cv2',
            'networkx',
        ],

        keywords=['python', 'TDA'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX :: Linux",
        ]
)
