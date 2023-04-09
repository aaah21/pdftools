from setuptools import setup, find_packages
import sys
import os

REQUIRES = ['PyPDF2']
CURRENT_PATH = os.path.join(os.path.dirname(__file__))
sys.path.insert(1, CURRENT_PATH)

setup(
    name='pdftools',
    version='1.0.0',
    url='https://github.com/aaah21/pdftools.git',
    author='Aleandro Andrea',
    author_email='aaah1976@gmail.com',
    description='Tool to manipulate PDF Files',
    packages=find_packages(),
    install_requires=REQUIRES,
)