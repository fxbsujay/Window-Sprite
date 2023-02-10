""""
# version:python 3.81
# -*- coding:utf-8 -*-

--------------------
# @Author       : fxbsujay@gmail.com
# @Time         : 10:44 2023/2/09
# @Version      : 1.0.0
# @Description  : Image OCR Engine
--------------------
"""

from enum import Enum


class ScriptType(Enum):
    json = 'json'
    excel = 'excel'


class EngFlag(Enum):
    """引擎运行状态标志"""
    none = 0  # 不在运行
    initializing = 1  # 正在启动
    waiting = 2  # 待命
    running = 3  # 工作中

