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
import time
import threading
from typing import List
from task.wx_api import WeChat

lock = threading.Lock()


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
        self._wxMessageLoadList: dict = {}
        task = threading.Thread(target=self.monitor_task)
        task.setDaemon(True)
        task.start()

    def message_handle(self):
        """
            处理消息
        """
        if bool(self._wxMessageLoadList):
            for name in self._wxMessageLoadList:
                if self._wxMessageLoadList[name]:
                    self._wxApi.open_session(name)
                    messages = self._wxApi.get_all_message()
                    for item in messages[len(messages) - self._wxMessageLoadList[name]:]:
                        # 搜索字库 回复消息
                        print(item.text)
                        self.set_unread_message(name, self._wxMessageLoadList[name] - 1)
            self._wxApi.open_session("文件传输助手")

    def set_unread_message(self, name: str, number: int):
        """
            更新未读消息数
        """
        lock.acquire()
        self._wxMessageLoadList[name] = number
        lock.release()

    def monitor_unread_message(self):
        """
            更新
        """
        unreadMessageUsers = self._wxApi.get_unread_message_users()
        if bool(unreadMessageUsers):
            for name in unreadMessageUsers:
                self.set_unread_message(name, unreadMessageUsers[name])

    def monitor_task(self):
        """
            实时监听新消息
        """
        while True:
            time.sleep(5)
            self.monitor_unread_message()


if __name__ == '__main__':
    w = WxSprite([])
    while True:
        time.sleep(5)
        w.message_handle()
