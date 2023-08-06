#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/3/19 17:13
# @Author : 詹荣瑞
# @File : utils.py
# @desc : 本代码未经授权禁止商用
from bonerator.content.command import Command, CommandLine
import hashlib
command_title = Command("title")
command_author = Command("author")
command_make_title = Command("maketitle")
command_use_package = Command("usepackage")
command_label = Command("label")
command_caption = Command("caption")
command_include_graphics = Command("includegraphics[width=0.8\\textwidth]")
commandline_centering = CommandLine("centering")
commandline_newpage = CommandLine("newpage")


def str_hash(string: str):
    return hashlib.md5(string.encode("utf-8")).hexdigest()
