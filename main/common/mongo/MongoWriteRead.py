#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : write_mongo.py.py
@Author: Fengjicheng
@Date  : 2019/9/17
@Desc  : MongoDB读写函数
'''
import traceback
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from MongoConn import *

my_conn = MongoConn()

def check_connected(conn):
    # 检查是否连接成功
    if not conn.connected:
        raise NameError('stat:connected Error')


def insert(table, value):
    # 可以使用insert直接一次性向mongoDB插入整个列表，也可以插入单条记录，但是'_id'重复会报错
    try:
        check_connected(my_conn)
        my_conn.db[table].insert(value, continue_on_error=True)
    except Exception:
        print(traceback.format_exc())


def save(table, value):
    # 一次操作一条记录，根据‘_id’是否存在，决定插入或更新记录
    try:
        check_connected(my_conn)
        my_conn.db[table].save(value)
    except Exception:
        print(traceback.format_exc())



def update(table, conditions, value, s_upsert=False, s_multi=False):
    try:
        check_connected(my_conn)
        my_conn.db[table].update(conditions, value, upsert=s_upsert, multi=s_multi)
    except Exception:
        print(traceback.format_exc())


def upsert_mary(table, datas):
    # 批量更新插入，根据‘_id’更新或插入多条记录。
    # 把‘_id’值不存在的记录，则插入数据库
    # 如果更新的字段在mongo中不存在，则直接新增一个字段
    try:
        # my_conn = MongoConn()
        check_connected(my_conn)
        bulk = my_conn.db[table].initialize_ordered_bulk_op()
        for data in datas:
            _id = data['_id']
            bulk.find({'_id': _id}).upsert().update({'$set': data})
        bulk.execute()
    except Exception:
        print(traceback.format_exc())

# def upsert_mary_field(table, datas):
#     # 批量更新插入，根据指定字段更新或插入多条记录。
#     # 把‘_id’值不存在的记录，则插入数据库
#     # 如果更新的字段在mongo中不存在，则直接新增一个字段
#     try:
#         # my_conn = MongoConn()
#         check_connected(my_conn)
#         bulk = my_conn.db[table].initialize_ordered_bulk_op()
#         for data in datas:
#             _id = data['_id']
#             bulk.find({'_id': _id}).upsert().update({'$set': data})
#         bulk.execute()
#     except Exception:
#         print(traceback.format_exc())


def upsert_one(table, data):
    # 更新插入，根据‘_id’更新一条记录，如果‘_id’的值不存在，则插入一条记录
    try:
        # my_conn = MongoConn()
        check_connected(my_conn)
        query = {'_id': data.get('_id', '')}
        if not my_conn.db[table].find_one(query):
            my_conn.db[table].insert(data)
        else:
            data.pop('_id')  # 删除'_id'键
            my_conn.db[table].update(query, {'$set': data})
    except Exception:
        print(traceback.format_exc())


def find_one(table, value):
    # 根据条件进行查询，返回一条记录
    try:
        check_connected(my_conn)
        return my_conn.db[table].find_one(value)
    except Exception:
        print(traceback.format_exc())


def find(table, value):
    # 根据条件进行查询，返回所有记录
    try:
        check_connected(my_conn)
        return my_conn.db[table].find(value, no_cursor_timeout=True)
    except Exception:
        print(traceback.format_exc())


def select_colum(table, value, colum):
    # 查询指定列的所有值
    try:
        check_connected(my_conn)
        return my_conn.db[table].find(value, {colum: 1})
    except Exception:
        print(traceback.format_exc())
