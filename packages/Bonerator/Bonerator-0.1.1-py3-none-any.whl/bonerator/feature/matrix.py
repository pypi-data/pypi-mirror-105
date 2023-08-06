#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/1/25 10:42
# @Author : 詹荣瑞
# @File : matrix.py
# @desc : 本代码未经授权禁止商用
from bonelate import render, parse

template = r"""
\left{{lb}}\begin{matrix}
{{!mat}}
  {{!.:&}} {{.}} {{/.}}\\
{{/mat}}
\end{matrix}\right{{rb}}
"""

print(parse(template))
print(render(template, {
    "lb": "(",
    "rb": "]",
    "mat": [[1, 2, 3, 4.6666], [2, 3, 4, 5], [2, 3, 4, 5]],
}))
