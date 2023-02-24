""""
# version:python 3.81
# -*- coding:utf-8 -*-

--------------------
# @Author       : fxbsujay@gmail.com
# @Time         : 11:12 2023/2/24
# @Version      : 1.0.0
# @Description  : 微信自动回复、聊天机器人 微信版本 3.9
--------------------
"""
import time
from typing import List

import uiautomation


class WeChat:

    def __init__(self):
        self.controller = uiautomation.WindowControl(ClassName='WeChatMainWndForPC')
        self.sessions = self.controller.ListControl(Name='会话')
        self.searchBox = self.controller.EditControl(Name='搜索')
        self.messages = self.controller.ListControl(Name='消息')
        self.sessionNameList: List[str] = []


    def refresh_sessions(self, reset: bool = False) -> List[str]:
        """
            获取当前微信窗口所展示的所有会话
            For Example: ['文件传输助手', ’微信支付‘, '微信团队', '相亲相爱一家人', '23考研群', .... ]
        """

        if reset:
            self.sessionNameList = []

        sessionNameList: List[str] = []
        sessionItem = self.sessions.ListItemControl()

        while sessionItem:

            name = sessionItem.Name
            if name not in self.sessionNameList:
                self.sessionNameList.append(name)

            if name not in sessionNameList:
                sessionNameList.append(name)
            sessionItem = sessionItem.GetNextSiblingControl()

        return sessionNameList


    def open_session(self, name: str, scrollTimes: int = 10) -> bool:
        """
            打开某个会话
            :param name         会话窗口名称
            :param scrollTimes  微信左侧滚轮向下滑动查找会话次数
        """

        def scroll_to():

            isUp = False
            lastWheelNames = ['0']

            for i in range(scrollTimes):
                names = self.refresh_sessions()
                if name not in names:
                    if not isUp and lastWheelNames and names[0] == lastWheelNames[0]:
                        isUp = True
                    lastWheelNames = names
                    if isUp:
                        self.sessions.WheelUp(wheelTimes=5, waitTime=0.1 * i)
                    else:
                        self.sessions.WheelDown(wheelTimes=5, waitTime=0.1 * i)
                else:
                    time.sleep(0.5)
                    self.sessions.ListItemControl(Name=name).Click(simulateMove=False)
                    return True
            return False

        if scroll_to():
            return True

        self.search_session(name)
        return scroll_to()


    def search_session(self, name: str):
        """
            搜索某个会话
            :param name 会话名称
        """
        self.controller.SetFocus()
        time.sleep(0.2)
        self.controller.SendKeys('{Ctrl}f', waitTime=1)
        self.searchBox.SendKeys(name, waitTime=1.5)
        self.searchBox.SendKeys('{Enter}')


    def load_more_message(self, index=0.1):
        """
            加载当前会话的所有历史消息记录到内存
            :param index 消息向上滚动次数 默认 50
        """
        index = 0.1 if index < 0.1 else 1 if index > 1 else index
        self.messages.WheelUp(wheelTimes=int(500 * index), waitTime=0.1)



if __name__ == '__main__':
    w = WeChat()
    w.refresh_sessions()
    a = w.open_session('企业微信')
    print(a)
    a = w.open_session('文件传输助手')
    print(a)