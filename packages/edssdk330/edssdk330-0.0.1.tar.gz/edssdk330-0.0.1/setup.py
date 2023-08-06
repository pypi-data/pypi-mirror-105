#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： hj
# datetime： 2021/5/7 0007 下午 3:17 
# ide： PyCharm2020.1.3


from setuptools import setup, find_packages
import setuptools

setuptools.setup(
    name="edssdk330",
    version="0.0.1",

    author="hj",
    author_email="1599712264@qq.com",
    description="eds sdk",
    long_description="eds sdk for python",
    url="http://hj.me",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['pymysql>=0.10.0','retrying==1.3.3','xlrd>=1.2.0','openpyxl>=3.0.5'],
    python_requires='>=3'
)
# setup(
#     name="edssdk",
#     version="0.0.1",
#     # keywords=("pip", "datacanvas", "eds", "hj","edssdk"),
#     keywords=["pip", "datacanvas", "eds", "hj","edssdk"],
#     description="eds sdk",
#     long_description="eds sdk for python",
#     license="MIT Licence",
#
#     url="http://hj.me",
#     author="hj",
#     author_email="1599712264@qq.com",
#
#     # packages=find_packages('edssdk'),
#     # package_dir={'':'edssdk'},
#     # package_data={'':['*.py']},
#     packages=find_packages(),
#     include_package_data=True,
#     platforms="any",
#     install_requires=[],
#
#     scripts=[],
#     py_modules=["edssdk.help"]
# )
