import json
from typing import List


class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


def dict_to_object(dictObj):
    """
    字典转对象
    :param dictObj: dic对象
    :return: obj
    """
    # 支持嵌套类型
    if isinstance(dictObj, list):
        insts = []
        for i in dictObj:
            insts.append(dict_to_object(i))
        return insts

    if not isinstance(dictObj, dict):
        return dictObj
    inst = Dict()
    for k, v in dictObj.items():
        inst[k] = dict_to_object(v)
    return inst


def json_to_object(json_str: str):
    """
    json字符串转对象
    :param json_str: json字符串
    :return: obj
    """
    return dict_to_object(json.loads(json_str))
