# -*- coding: utf-8 -*-
"""
Created on Tue May  4 10:58:39 2021

@author: AbdusSalam
"""
from setuptools import setup, find_packages
import os

here = os.path.dirname(os.path.abspath(__file__))

with open(f'{here}/README.md', 'r') as fh:
    long_description = fh.read()
setup(
    name="tquota",
    version="0.0.2",
    author="Aljbri AbdusSalam",
    author_email="mr.aljbri@gmail.com",
    description="processing timer module for running on the cloud with the quota time like Kaggle and colab",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aljbri/tquota",
	project_urls={
        "Bug Tracker": "https://github.com/aljbri/tquota/issues",
    },
	packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    keywords='timer, quota, kaggle, colab',
    #python_requires='>=3.6',
)
