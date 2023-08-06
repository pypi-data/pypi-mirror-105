#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/5/2 22:30
# @Author : 詹荣瑞
# @File : btex_bonelate.py
# @desc : 本代码未经授权禁止商用
from bonelate import render, parse

template = r"""
\begin{table}[htbp]
\centering 
\caption{{{title}}} 
\label{{{label}}} 
\begin{tabular}{{{table-args}}}
  \toprule
  {{!table}}
    {{!.}}{{.}}&{{/.}}\\
  {{/table}}
  \bottomrule
\end{tabular} 
\end{table} 
"""

print(render(template, {
    "title": "bonelate-demo",
    "label": "bonelate-demo",
    "table-args": "ccccc",
    "table": [[1, 2, 3, 4.6666], r"\midrule", [2, 3, 4, 5], [2, 3, 4, 5]],
}))
