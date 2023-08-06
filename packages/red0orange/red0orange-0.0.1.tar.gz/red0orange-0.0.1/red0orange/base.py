#!/home/hdh3/anaconda3/bin/python
# encoding: utf-8
"""
@author: red0orange
@file: base.py
@time:  3:07 PM
@desc:
"""
import os


class SingleModel(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,'__instance__'):
            cls.__instance__ = super(SingleModel, cls).__new__(cls)
        return cls.__instance__

    def init(self):
        pass

