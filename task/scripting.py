""""
# version:python 3.81
# -*- coding:utf-8 -*-

--------------------
# @Author       : fxbsujay@gmail.com
# @Time         : 11:12 2023/08/06
# @Version      : 1.0.0
# @Description  : 读取脚本文件，脚本编排
--------------------
"""
import json
from typing import List
from utils.tools import read_file


class Script:
    """
        Script Model
    """

    def __init__(self, type: int, value: str, reset: int = 0):
        """
        type:    脚本类型
        value:   脚本内容
        reset:   脚本重复执行次数
        """
        self._type = type
        self._value = value
        self._reset = reset

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value

    @property
    def reset(self):
        return self._reset

    def __str__(self):
        return 'type={},value={},reset={}'.format(self._type, self._value, self._reset)


def inspect_json(filename: str) -> List[Script]:
    """
    :param filename: json脚本文件
        For Example : [ { "type": 1, "value": "flag.png", "reset": 0} ]
    """
    jsonStr = read_file(filename)
    jsonData: List[Script] = []
    if len(jsonStr) > 0:
        dataList = json.loads(jsonStr)
        for item in dataList:
            jsonData.append(Script(item['type'], item['value'], item['reset']))
    return jsonData
