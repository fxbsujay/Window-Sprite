""""
# version:python 3.81
# -*- coding:utf-8 -*-

--------------------
# @Author       : fxbsujay@gmail.com
# @Time         : 10:44 2023/2/09
# @Version      : 1.0.0
# @Description  : 枚举
--------------------
"""

from enum import Enum


class WxMessageHeights(Enum):
    """
        微信消息高度类型
            sys     系统提示消息
            time    消息发送时间提示
            recall  消息撤回
    """
    sys = 33
    time = 34
    recall = 117


class WxMessageType(Enum):
    """发送的消息类型"""
    file = '[文件]'
    image = '[图片]'
    video = '[视频]'
    music = '[音乐]'
    link = '[链接]'


class ScriptType(Enum):
    json = 'json'
    excel = 'excel'


class EngFlag(Enum):
    """引擎运行状态标志"""
    none = 0  # 不在运行
    initializing = 1  # 正在启动
    waiting = 2  # 待命
    running = 3  # 工作中


class PurposeType(Enum):
    """App主要用途"""
    daily = '日常使用'  # 日常使用
    weChat = '微信客服'  # 微信客服
