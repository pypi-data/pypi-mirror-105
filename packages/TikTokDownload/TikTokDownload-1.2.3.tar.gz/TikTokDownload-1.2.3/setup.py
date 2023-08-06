#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='TikTokDownload',
    version='1.2.3',
    description=(
        '一个很方便的下载中国版抖音无水印视频以及用户主页视频的包。Tiktok China is a very convenient download of Chinese version of the video without watermark and video.'
    ),
    author='JohnserfSeed',
    author_email='2080979987@qq.com',
    maintainer='JohnserfSeed',
    maintainer_email='2080979987@qq.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/Johnserf-Seed/TikTokDownload',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'requests>=2.23.0',
    ],
)