from __future__ import print_function
from setuptools import setup, find_packages
import sys

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()  

setup(
    name="WPS2OpenGMS",
    version="1",
    author="WYJQ",
    author_email="371252847@qq.com",
    description="This program is used to automatically encapsulate WPS models using the OpenGMS method.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://www.baidu.com/",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Environment :: Web Environment",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
            'lxml',  
            'requests'   
    ],
    zip_safe=True,
)
