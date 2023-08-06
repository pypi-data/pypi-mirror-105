#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import division
import json
import os , sys, platform,shutil, cmd
import inspect
import datetime
import functools

import numpy as np

from functools import lru_cache
from functools import wraps


class Singleton(object):
    _instance = None
    _is_init = False
    def __new__(cls, *args,**kwargs):
        if not cls._instance:
            cls._instance = super(Singleton,cls).__new__(cls,*args,**kwargs)
        return cls._instance
    

def Singleton_wraps(cls):
    _instance = {}
    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]
    return wrapper


class FormulaException(Exception):
    pass


def wrap_formula_exc(func):
    def wrapper(*args, **kwargs):
        try:
            # print(func, args, kwargs)
            return func(*args, **kwargs)
        except (ValueError, IndexError) as e:
            raise FormulaException(e)

    return wrapper


def getsourcelines(func):
    try:
        source_code = "".join(inspect.getsourcelines(func)[0]).strip()
        return source_code
    except:
        return ""


def get_int_date(date):
    if isinstance(date, int):
        return date

    try:
        return int(datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%Y%m%d"))
    except:
        pass

    try:
        return int(datetime.datetime.strptime(date, "%Y%m%d").strftime("%Y%m%d"))
    except:
        pass

    if isinstance(date, (datetime.date)):
        return int(date.strftime("%Y%m%d"))

    raise ValueError("unknown date {}".format(date))


def get_str_date_from_int(date_int):
    try:
        date_int = int(date_int)
    except ValueError:
        date_int = int(date_int.replace("-", ""))
    year = date_int // 10000
    month = (date_int % 10000) // 100
    day = date_int % 100

    return "%d-%02d-%02d" % (year, month, day)


def get_date_from_int(date_int):
    date_str = get_str_date_from_int(date_int)

    return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()


def rolling_window(a, window):
    '''
    copy from http://stackoverflow.com/questions/6811183/rolling-window-for-1d-arrays-in-numpy
    '''
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1], )
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


def handle_numpy_warning(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with np.errstate(invalid='ignore'):
            return func(*args, **kwargs)
    return wrapper


# diffrence OS path
path = os.path.expanduser('~')
rq_path = '{}{}{}'.format(path, os.sep, '.rrsdk')
#print(platform.system(),path, rq_path)

def get_path_file_name(path_name, file_name):
    # diffrence OS path
    if platform.system() == 'Linux':
        path_name_chg = ''.join([rq_path,'/' ,path_name, '/', file_name])
    if platform.system() == 'Windows':
        path_name_chg =  ''.join([rq_path,'\\', path_name, '\\',file_name])
    print(path_name_chg)
    return path_name_chg

path_setting = get_path_file_name('setting','config.json')


@Singleton_wraps
class Setting(object):
    def __init__(self, path_config=path_setting):
        self.path_config = path_config
        
    def setting(self):
        config = open(self.path_config)
        return json.load(config)


setting = Setting().setting()
#print(setting)

if __name__ == '__main__':
    s = Setting()
    #print(id(s), id(Setting()))
    print(s.setting()['TSPRO_TOKEN'])

    


