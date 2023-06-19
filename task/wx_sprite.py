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
import xlrd
from utils.tools import get_join_pardir

lock = threading.Lock()


def char_similarity(word, entry):
    """
        判断两个字符串的相似度
    """
    hash_str = {}
    for char in word:
        hash_str[hash(char)] = char

    same_chars = []
    for char in entry:
        if hash(char) in hash_str and char not in same_chars:
            same_chars.append(char)

    return len(same_chars) / len(entry)


def load_entries(filename: str):
    """
        加载消息回复的词条
    """
    wb = xlrd.open_workbook(filename=filename)
    sheet = wb.sheet_by_index(0)
    print(sheet.nrows)
    index = 0
    while index < sheet.nrows:
        print('-------')
        row = sheet.row(index)
        print(row)
        index += 1


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
            更新监听信息
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
    load_entries(get_join_pardir("doc\\wx_entries.xls"))
