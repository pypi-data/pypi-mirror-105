'''
Author: GongZiyao
Date: 2021-05-10 11:40:52
LastEditors: GongZiyao
LastEditTime: 2021-05-11 09:36:12
'''
#!/usr/bin/env python
# coding: utf-8
import threading
import pickle
import hashlib


class Singleton:
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(Singleton, "_instance"):
                    Singleton._instance = object.__new__(cls)
        return Singleton._instance


class MultitionInstanceFactory(Singleton):

    _instance_lock = threading.Lock()
    _instance_dict = {}

    @classmethod
    def get_instance(cls, class_obj, *args, **kwargs):
        assert isinstance(class_obj, type)
        class_name = class_obj.__name__
        params_md5 = hashlib.md5(pickle.dumps((args, kwargs))).hexdigest()
        cls._set_dict_value_if_absent(cls._instance_dict, class_name, {})
        cls._set_dict_value_if_absent(
            cls._instance_dict[class_name], params_md5, class_obj(*args, **kwargs))
        return cls._instance_dict[class_name][params_md5]

    @classmethod
    def _set_dict_value_if_absent(cls, check_dict, key, value):
        if key not in check_dict:
            with cls._instance_lock:
                if key not in check_dict:
                    check_dict[key] = value
