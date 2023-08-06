#!/home/hdh3/anaconda3/bin/python
# encoding: utf-8
"""
@author: red0orange
@file: args.py
@time:  11:10 PM
@desc:
"""
import argparse
import ast
import os
import time
import numpy as np
import torch
import shutil
import random
from red0orange.base import SingleModel


def get_class_attr(c):
    name_list = [i for i in dir(c) if not i.startswith('__')]
    result = {k:getattr(c, k) for k in name_list}
    return result


class BaseParam(object):
    """对应parser.add_argument的参数，封装起来方便参数的添加"""
    def __init__(self, mtype, default=None, mhelp=None):
        self.mtype = mtype
        self.mhelp = mhelp
        self.default = default
        if not isinstance(self.default, self.mtype):
            raise BaseException('默认值类别错误')
        pass


class BaseOption(object):
    gpu = BaseParam(str, '0', '多gpu的情况下使用哪个gpu')
    seed = BaseParam(int, 28, '使用的随机种子')
    outcome_root = BaseParam(str, 'outcomes')
    description = BaseParam(str, '')
    name = BaseParam(str, '')
    checkout = BaseParam(str, '')
    epochs = BaseParam(int, 100)
    batch_size = BaseParam(int, 32)
    lr = BaseParam(float, 1e-3)
    device = BaseParam(str, 'cuda')


class Args(SingleModel):
    def init(self, option):
        self.parse_args(option)

        np.random.seed(self.seed)
        torch.manual_seed(self.seed)
        torch.cuda.manual_seed_all(self.seed)
        random.seed(self.seed)
        torch.backends.cudnn.benchmark = False
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.enabled = True

        os.environ["CUDA_VISIBLE_DEVICES"] = self.gpu

        if self.name == '':
            self.model = '' if not hasattr(self, 'model') else self.self.model
            self.name = self.model + time.strftime('(%m-%d_%H:%M)', time.localtime(time.time()))
        else:
            self.name += time.strftime('(%m-%d_%H:%M)', time.localtime(time.time()))
        # 动态赋值一个当前任务的保存文件夹路径到self里面
        if self.description == '':
            self.save_root = os.path.join(self.outcome_root, self.name)
        else:
            self.save_root = os.path.join(self.outcome_root, self.description, self.name)

        if os.path.exists(self.save_root):
            shutil.rmtree(self.save_root)
        os.makedirs(self.save_root)

        return self

    def parse_args(self, option):
        parser = argparse.ArgumentParser()
        for name, param in get_class_attr(option).items():
            if param.mtype == bool:
                parser.add_argument(f'--{name}', type=ast.literal_eval, default=param.default, help=param.mhelp)
            else:
                parser.add_argument(f'--{name}', type=param.mtype, default=param.default, help=param.mhelp)
        args_ = parser.parse_args()
        for key, value in get_class_attr(args_).items():
            setattr(self, key, value)
        pass

    def get_args(self):
        return {k:getattr(self, k) for k in self.__dict__.keys() if not k.startswith(('_', '__'))}


option = Args()
