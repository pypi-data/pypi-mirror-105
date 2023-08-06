from setuptools import setup, find_packages
import codecs
import os



VERSION = '1.0.4'
DESCRIPTION = 'Python Toolkit to extract tiles from a Whole Slide Image'
LONG_DESCRIPTION = 'Python package to extrac tiles from a Whole Slide Image '

# Setting up
setup(
    name="wsiPy",
    version=VERSION,
    author="Ronan White",
    author_email="<ronan.white@hotmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['Pillow','openslide-python','scikit-image','scikit-learn','scipy'],
    keywords=['python', 'Whole Slide Images'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
	"Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)