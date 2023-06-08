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
import uiautomation
from utils.enums import WxMessageHeights
from typing import List


class WxMessage:
    """
      Message Model
    """

    def __init__(self, user: str, text: str, runtimeId: str):
        """
        :param user:        消息发送方
        :param text:        消息内容
        :param runtimeId:   消息Id
        """
        self._user = user
        self._text = text
        self._runtimeId = runtimeId

    @property
    def user(self):
        return self._user

    @property
    def text(self):
        return self._text

    @property
    def runtimeId(self):
        return self._runtimeId

    def __str__(self):
        return 'type={},text={},runtimeId={}'.format(self._user, self._text, self._runtimeId)


class WeChat:

    def __init__(self):
        self.controller = uiautomation.WindowControl(ClassName='WeChatMainWndForPC')
        self.sessions = self.controller.ListControl(Name='会话')
        self.searchBox = self.controller.EditControl(Name='搜索')
        self.messages = self.controller.ListControl(Name='消息')
        self.messageInputBox = self.controller.EditControl(Name="输入")
        self.sessionNameList: List[str] = []
        self.controller.SetTopmost(True)

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

    def open_session(self, name: str, scrollTimes: int = 3) -> bool:
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
            消息加载更多
            :param index 消息向上滚动次数
        """
        index = 0.1 if index < 0.1 else 1 if index > 1 else index
        self.messages.WheelUp(wheelTimes=int(500 * index), waitTime=0.1)

    def get_all_message(self) -> List[WxMessage]:
        """
            查询所有的消息
        """
        messageList: List[WxMessage] = []
        for item in self.messages.GetChildren():
            rectangleHeight = item.BoundingRectangle.height()
            text = item.Name
            runtimeId = ''.join([str(i) for i in item.GetRuntimeId()])

            if rectangleHeight not in [member.value for member in WxMessageHeights]:
                Index = 1
                uiautomation.SetGlobalSearchTimeout(0)
                user = item.ButtonControl(foundIndex=Index)

                try:
                    while True:
                        if user.Name == '':
                            Index += 1
                            user = item.ButtonControl(foundIndex=Index)
                        else:
                            break
                    messageList.append(WxMessage(user.Name, text, runtimeId))
                except LookupError:
                    print('未找到发送人')
                uiautomation.SetGlobalSearchTimeout(10)
        return messageList

    def send_message(self, message: str, clear: bool = True):
        """
            向当前开发的微信窗口发送消息
            message: 消息内容
            clear:   是否清空已编辑的内容
        """

        self.controller.SwitchToThisWindow()
        if clear:
            self.messageInputBox.SendKeys('{Ctrl}a', waitTime=0)
        self.messageInputBox.SendKeys(message, waitTime=0)
        self.messageInputBox.SendKeys('{Enter}', waitTime=0)


if __name__ == '__main__':
    w = WeChat()
    w.refresh_sessions()
    w.open_session("文件传输助手")
    messages = w.get_all_message()
    for msg in messages:
        print(str(msg))
    w.send_message("你好")
