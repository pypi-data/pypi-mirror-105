#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='jojo_tmp',
    version='0.0.1',
    author='Joe_yoy',
    author_email='Joe_yoy@outlook.com',
    url='https://zhuanlan.zhihu.com/p/26159930',
    description=u'吃枣药丸',
    license='MIT',
    packages=['jojo'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'eat=jojo:eat',
            'jump=jojo:jump'
        ]
    }
)