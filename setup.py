#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bionic-message-tools",
    version="1.0.6",
    author="Timo Schwarzer",
    author_email="timo.schwarzer@festo.com",
    description="The Festo bionic message tools",    
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.festo.com/group/de/cms/10156.htm",
    packages=setuptools.find_packages('include'),    
    package_dir={'':'include'},    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU GPL v3.0",
        "Operating System :: OS Independent",
    ],
    install_requires=[        
        'pyserial==3.4',
        'paho-mqtt'
    ],
)