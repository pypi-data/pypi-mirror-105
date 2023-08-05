###############################################################################
#####   Setup.py - installs all the required packages and dependancies    #####
###############################################################################

import pathlib
from setuptools import setup, find_packages
import sys

#ensure python version is greater than 3
if sys.version_info[0] < 3:
    sys.exit('Python 3 is the minimum version requirement')

HERE = pathlib.Path(__file__).parent

README = (HERE / 'README.md').read_text()

setup(name='pySAR',
      version='0.0.3',
      description='A Python package used to analysis Protein Sequence Activity Relationships',
      long_description = README,
      long_description_content_type = "text/markdown",
      url = "https://github.com/amckenna41/pySAR",
      author='Adam McKenna',
      author_email='amckenna41@qub.ac.uk',
      license='MIT',
      classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
    ],
      install_requires=[
          'numpy==1.16.6',
          'pandas',
          'scipy',
          'delayed',
          'scikit-learn==0.24.1',
          'requests',
          'matplotlib',
          'seaborn',
          'tqdm'
      ],
     # packages=find_packages(), #create Manifest file to ignore results folder in dist
     packages=find_packages(exclude=["Results"]),
     include_package_data=True,
     zip_safe=False)
