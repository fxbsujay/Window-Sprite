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
from utils.tools import get_join_pardir, is_file
from utils.snowflake import snowflake

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
    index = 1
    tagList: dict = {}
    entriesList: dict = {}
    while index < sheet.nrows:
        tagId = snowflake.generate_id()
        row = sheet.row(index)
        tags = row[0]
        for tag in str(tags.value).split(','):
            tagList[tag] = tagId
        colIndex = 1
        entries: list = []
        while colIndex < len(row):
            textType = 1
            if is_file(row[colIndex].value):
                textType = 2
            entries.append({textType: row[colIndex].value})
            colIndex += 1
        entriesList[tagId] = entries
        index += 1

    return tagList, entriesList


class WxSprite:

    def __init__(self, users: List[str], filename):
        self._wxApi = WeChat()
        self._wxMessageLoadList: dict = {}
        task = threading.Thread(target=self.monitor_task)
        task.setDaemon(True)
        task.start()
        tagList, entriesList = load_entries(filename)
        self._tags: dict = tagList
        self._entries: dict = entriesList

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
                        responseMessage = self.search_entries(item.text)
                        if responseMessage:
                            self.response_message_list(responseMessage)
                        self.set_unread_message(name, self._wxMessageLoadList[name] - 1)
            self._wxApi.open_session("文件传输助手")


    def search_entries(self, text: str):
        for tag in self._tags:
            if char_similarity(text, tag) > 0.7:
                return self._entries[self._tags[tag]]
        return []

    def response_message_list(self, responseMessage):
        index = 0
        clear = True
        sendImmediately = False
        while index < len(responseMessage):
            if index == len(responseMessage)-1:
                sendImmediately = True
            if index == 1:
                clear = False
            for msgType in responseMessage[index]:
                if msgType == 2:
                    self._wxApi.send_file(responseMessage[index][msgType], sendImmediately=sendImmediately, clear=clear)
                else:
                    self._wxApi.send_message(responseMessage[index][msgType], clear=clear, sendImmediately=sendImmediately)
            index += 1


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
    wx = WxSprite([], get_join_pardir("doc\\wx_entries.xls"))
    while True:
        time.sleep(2)
        wx.message_handle()
