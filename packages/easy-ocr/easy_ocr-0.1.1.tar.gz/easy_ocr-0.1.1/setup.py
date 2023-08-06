#encoding:utf-8
import os
from setuptools import setup, find_packages

project_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

def read_file(filename):
    filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                            filename)
    if os.path.exists(filepath):
        return open(filepath).read()
    else:
        return ''

setup(
    name=project_name,
    version="0.1.1",
    keywords=('ocr'),
    description="a tool for ocr api service",
    long_description=read_file('README.rst'),
    platforms="any",
    install_requires=['requests>=2.0.0'],
    packages = find_packages()
)

