#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/3/18 21:43
# @Author : 詹荣瑞
# @File : setup.py
# @desc : 本代码未经授权禁止商用
import bonerator
from setuptools import setup, find_packages

with open("README.md", "r", encoding='UTF-8') as file:
    long_description = file.read()

setup(
    name="Bonerator",
    version=bonerator.__version__,
    author="六个骨头",
    author_email="2742392377@qq.com",
    description="""
    Bonerator 是一个自动生成LaTeX代码的辅助库，
    你也可以使用Python高效的完成LaTeX文档的编写，
    同时支持将MarkDown、Excel等文件转换成LaTeX代码。
    """,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zrr1999/bonerator",
    # 你要安装的包，通过 setuptools.find_packages 找到当前目录下有哪些包
    packages=find_packages(),
    package_data={
        '': ['*.txt'],
        # 包含demo包data文件夹中的 *.dat文件
        'demo': ['data/*.dat'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    platforms="any",
    install_requires=["bonelate"],
    entry_points={
    }
)
