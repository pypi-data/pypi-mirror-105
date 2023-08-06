#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/1/24 17:08
# @Author : 詹荣瑞
# @File : environment.py
# @desc : 本代码未经授权禁止商用
from bonetex.content.content import ContentList, ContentBase
from bonelate import render
from typing import Tuple, Union


class Environment(ContentBase):
    template = (
        r"{{indent}}\begin{{{name}}}{{option}}"
        "\n{{!contents}}{{.}}{{/contents}}\n"
        r"{{indent}}\end{{{name}}}"
    )

    def __init__(self, name, children: ContentList = None, option: Union[Tuple[list, dict], str] = None):
        self.name = name
        self.children = children or ContentList()
        self.dict = {
            "type": "environment",
            "name": name,
            "option": option,
            "indent": "",
            "contents": "",
        }

    def __iter__(self):
        for out in self.dict["children"]:
            yield out

    def latex(self, indent=""):
        self.dict["indent"] = indent
        self.dict["contents"] = self.children.latex(indent + "  ")
        return render(self.template, self.dict)


class FileEnvironment(Environment):

    def __init__(self, name, contents: ContentList = None, option: Tuple[list, dict] = None,
                 resources_folder=""):
        self.resources_folder = resources_folder
        super().__init__(name, contents, option)
