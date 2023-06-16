""""
# version:python 3.81
# -*- coding:utf-8 -*-

--------------------
# @Author       : fxbsujay@gmail.com
# @Time         : 11:12 2023/2/24
# @Version      : 1.0.0
# @Description  : 微信自动化工具，微信版本 3.9.5.81  仅支持 windows
--------------------
"""

import time
import uiautomation
from utils.enums import WxMessageHeights
from typing import List
from uiautomation import Control
import win32clipboard
import os


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
        return 'user={},text={},runtimeId={}'.format(self._user, self._text, self._runtimeId)


def clipboard_formats(unit=0, *units):
    units = list(units)
    win32clipboard.OpenClipboard()
    u = win32clipboard.EnumClipboardFormats(unit)
    win32clipboard.CloseClipboard()
    units.append(u)
    if u:
        units = clipboard_formats(u, *units)
    return units


def copy_dict() -> dict:
    copyDict = {}
    for i in clipboard_formats():
        if i == 0:
            continue
        win32clipboard.OpenClipboard()
        try:
            content = win32clipboard.GetClipboardData(i)
            win32clipboard.CloseClipboard()
        except:
            win32clipboard.CloseClipboard()
            raise ValueError
        if len(str(i)) >= 4:
            copyDict[str(i)] = content
    return copyDict


def split_message(message: Control) -> WxMessage:
    index = 1
    user = message.ButtonControl(foundIndex=index).Name
    text = message.Name
    runtimeId = ''.join([str(i) for i in message.GetRuntimeId()])

    if len(user):
        return WxMessage(user, text, runtimeId)

    try:
        while True:
            if message.ButtonControl(foundIndex=index).Name == '':
                index += 1
                user = message.ButtonControl(foundIndex=index).Name
            else:
                break
        return WxMessage(user, text, runtimeId)
    except LookupError:
        return WxMessage("未知发送人", text, runtimeId)


class WeChat:

    def __init__(self):
        self.controller = uiautomation.WindowControl(ClassName='WeChatMainWndForPC')
        self.sessions = self.controller.ListControl(Name='会话')
        self.searchBox = self.controller.EditControl(Name='搜索')
        self.messages = self.controller.ListControl(Name='消息')
        self.messageInputBox = self.controller.TextControl()
        self.sessionNameList: List[str] = []
        self.controller.SetTopmost(True)
        uiautomation.SetGlobalSearchTimeout(0)

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
            if "条新消息" in name:
                name = sessionItem.ButtonControl().Name

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
                    try:
                        self.sessions.ListItemControl(Name=name).Click(simulateMove=False)
                        return True
                    except LookupError:
                        for children in self.sessions.GetChildren():
                            if name == children.ButtonControl().Name:
                                children.ButtonControl().Click(simulateMove=False)
                                return True
            return False

        if scroll_to():
            return True

        self.search_session(name)
        return scroll_to()

    def get_unread_messages_number(self, name: str) -> int:
        """
            获取微信用户发来的未读消息数量
            :param name 会话名称
        """
        sessionItem = self.sessions.ListItemControl()

        while sessionItem:
            if name == sessionItem.ButtonControl().Name and sessionItem.PaneControl().GetChildren()[-1].Name:
                return int(sessionItem.PaneControl().GetChildren()[-1].Name)
            sessionItem = sessionItem.GetNextSiblingControl()
        return 0


    def get_unread_message_users(self) -> dict:
        """
            获取所有有未读消息的用户
        """
        usernames = {}
        self.controller.ButtonControl(Name="聊天").DoubleClick(simulateMove=False)
        sessionItem = self.sessions.ListItemControl()

        while sessionItem:
            name = sessionItem.Name
            if "条新消息" in name:
                usernames[sessionItem.ButtonControl().Name] = int(sessionItem.PaneControl().GetChildren()[-1].Name)
            sessionItem = sessionItem.GetNextSiblingControl()
        return usernames


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
        for children in self.messages.GetChildren():
            rectangleHeight = children.BoundingRectangle.height()
            if rectangleHeight not in [member.value for member in WxMessageHeights]:
                messageList.append(split_message(children))
        return messageList

    def get_last_message(self):
        """
            获取最后一条消息
        """
        message = self.messages.GetChildren()[-1]
        return split_message(message)

    def send_message(self, message: str, clear: bool = True):
        """
            向当前聊天窗口发送文消息
            message: 消息内容
            clear:   是否清空已编辑的内容
        """
        self.controller.SwitchToThisWindow()
        if clear:
            self.messageInputBox.SendKeys('{Ctrl}a', waitTime=0)
        self.messageInputBox.SendKeys(message, waitTime=0)
        self.messageInputBox.SendKeys('{Enter}', waitTime=0)

    def send_file(self, *filepath: str):
        """
            向当前聊天窗口发送文件
            not_exists: 如果未找到指定文件，继续或终止程序
            *filepath: 要复制文件的绝对路径
        """
        key = ''
        for file in filepath:
            file = os.path.realpath(file)
            key += '<EditElement type="3" filepath="%s" shortcut="" />' % file
        if not key:
            return 0

        copyDict = {
            '49949': b'<WeChatRichEditFormat><EditElement type="0"><![CDATA[ ]]></EditElement></WeChatRichEditFormat>\x00',
            '49950': b'<RTXRichEditFormat><EditElement type="0"><![CDATA[ ]]></EditElement></RTXRichEditFormat>\x00',
            '49951': b'<QQRichEditFormat><EditElement type="0"><![CDATA[ ]]></EditElement></QQRichEditFormat>\x00'
        }

        '''https://learn.microsoft.com/zh-cn/windows/win32/dataxchg/standard-clipboard-formats'''
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, '')
        win32clipboard.SetClipboardData(win32clipboard.CF_LOCALE, b'\x04\x08\x00\x00')
        win32clipboard.SetClipboardData(win32clipboard.CF_TEXT, b'')
        win32clipboard.SetClipboardData(win32clipboard.CF_OEMTEXT, b'')
        for i in copyDict:
            copyData = copyDict[i].replace(b'<EditElement type="0"><![CDATA[ ]]>', key.encode()).replace(b'type="0"',
                                                                                                         b'type="3"')
            win32clipboard.SetClipboardData(int(i), copyData)
        win32clipboard.CloseClipboard()
        self.send_message('{Ctrl}v')


if __name__ == '__main__':
    w = WeChat()
    print(w.get_unread_message_users())
    print(w.get_all_message())
