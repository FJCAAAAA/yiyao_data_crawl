#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : getkeyword.py
@Author: Fengjicheng
@Date  : 2020/1/8
@Desc  :
'''
import pickle
import json


def load_pickle(path):
    with open(path, 'rb') as f:
        return json.dumps(pickle.load(f), ensure_ascii=False)

if __name__ == '__main__':
    print(load_pickle('dise_sym_num_dict.p'))