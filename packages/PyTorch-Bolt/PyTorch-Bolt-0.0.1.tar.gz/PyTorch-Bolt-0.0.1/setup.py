#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools


with open('README.md', 'r', encoding='utf-8') as f:
    README = f.read()

setuptools.setup(
    name='PyTorch-Bolt',
    version='0.0.1',
    description='A simple PyTorch wrapper making multi-node multi-GPU training much easier on Slurm',
    author='Yi Zhang',
    author_email='yizhang.dev@gmail.com',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/yzhang-dev/PyTorch-Bolt',
    download_url='https://github.com/yzhang-dev/PyTorch-Bolt',
    packages=setuptools.find_packages(),
    keywords=[
        'pytorch', 'pytorch-template', 'ddp', 'distributed', 'slurm', 
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    license='MIT',
    python_requires='>=3.8',
    install_requires=[
        'torch==1.8.1',
        'torchvision==0.9.1',
        'tensorboard==2.4.1',
    ],
)
