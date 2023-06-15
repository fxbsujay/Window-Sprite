""""
# version:python 3.81
# -*- coding:utf-8 -*-

--------------------
# @Author       : fxbsujay@gmail.com
# @Time         : 11:12 2023/06/08
# @Version      : 1.0.0
# @Description  : 微信自动回复、聊天机器人 微信版本 3.9
--------------------
"""
from typing import List
from task.wx_api import WeChat


class WxMessageLoadInfo:
    """
         Message Model
       """

    def __init__(self, user: str, lastRuntimeId: str):
        """
        :param user:            消息发送方
        :param lastRuntimeId:   最后一条消息Id
        """
        self._user = user
        self._lastRuntimeId = lastRuntimeId

    @property
    def user(self):
        return self._user

    @property
    def runtimeId(self):
        return self._lastRuntimeId

    def __str__(self):
        return 'user={},lastRuntimeId={}'.format(self._user, self._lastRuntimeId)


class WxSprite:


    def __init__(self, users: List[str]):
        self._wxApi = WeChat()



