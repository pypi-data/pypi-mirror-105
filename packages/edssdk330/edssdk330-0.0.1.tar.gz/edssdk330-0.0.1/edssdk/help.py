#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： hj
# datetime： 2021/5/7 0007 下午 4:39 
# ide： PyCharm2020.1.3

def sum(*values):
    s = 0
    for v in values:
        i = int(v)
        s = s + i
    print(s)


def output():
    print('http://xiaoh.me')
