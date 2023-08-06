#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/5/10 16:54
# @Author  : UJN.Wenbin
# @FileName: setup.py
# @Software: PyCharm
import requests
from setuptools import setup, find_packages

filepath = 'README.md'

def md_to_rst(file, to_file):
    """
    将markdown格式转换为rst格式
    @param from_file: {str} markdown文件的路径
    @param to_file: {str} rst文件的路径
    """
    response = requests.post(
        url='http://c.docverter.com/convert',
        data={'to': 'rst', 'from': 'markdown'},
        files={'input_files[]': open(file, 'rb')}
    )

    if response.ok:
        with open(to_file, "wb") as f:
            f.write(response.content)
md_to_rst(filepath, 'README.rst')

setup(
    name="CXCFmsMC-binbin6106",
    version="1.0.2",
    author="Wenbin",
    author_email="zhangwenbin@mail.ujn.edu.cn",
    description="A pkg to operate mitsubishi PLC by MCProtocol.",
    long_description=open('README.rst', encoding='utf-8').read(),
    # long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10"
    ]
)
