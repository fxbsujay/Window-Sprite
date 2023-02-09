""""
# version:python 3.81
# -*- coding:utf-8 -*-

--------------------
# @Author       : fxbsujay@gmail.com
# @Time         : 11:32 2023/2/09
# @Version      : 1.0.0
# @Description  : Tools
--------------------
"""
import os
import time
import pyautogui
import win32con, win32gui, win32clipboard
from PIL import ImageGrab
from utils.config import Config
from utils.config import console
from PIL import Image
from io import BytesIO


def mouseClick(clickTimes, lOrR, img, reTry) -> None:
    """
    控制鼠标点击
    :param clickTimes: 点击次数
    :param lOrR:       鼠标左键还是右键
    :param img:        匹配相同的图片
    :param reTry:      重复次数
    """
    console.print("鼠标点击事件：鼠标键位=", lOrR, "img=", img, "点击次数=", clickTimes, "重复次数=", reTry, style="bold red")
    windowRect = Config.get('WindowRect')

    if reTry == 1:
        while True:
            location = pyautogui.locateCenterOnScreen(img, confidence=0.8, region=windowRect)
            if location is not None:
                pyautogui.click(location.x, location.y, clicks=clickTimes, interval=0.2, duration=0.2, button=lOrR)
                break
            time.sleep(0.1)
    elif reTry == -1:
        while True:
            location = pyautogui.locateCenterOnScreen(img, confidence=0.8, region=windowRect)
            if location is not None:
                pyautogui.click(location.x, location.y, clicks=clickTimes, interval=0.2, duration=0.2, button=lOrR)
            time.sleep(0.1)
    elif reTry > 1:
        i = 1
        while i < reTry + 1:
            location = pyautogui.locateCenterOnScreen(img, confidence=0.8, region=windowRect)
            if location is not None:
                pyautogui.click(location.x, location.y, clicks=clickTimes, interval=0.2, duration=0.2, button=lOrR)
                i += 1
            time.sleep(0.1)


def copy_image_to_clipboard(path: str):
    if not os.path.isfile(path):
        return
    """
    复制图片到剪切板
    
    :path: 图片路径
    """

    image = Image.open(path)
    output = BytesIO()
    image.save(output, 'BMP')
    data = output.getvalue()[14:]

    output.close()
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()


def application_screenshot_tool(name: str = "", path: str = Config.get("screenshotSavePath"), isSaveWindowRect: bool = False) -> None:
    """
    窗口截图工具
    :name 需要截图的窗口应用程序名称
    :path 截图保存的位置
    :isSaveWindowRect 是否需要将截图的窗口坐标保存下来
    """

    handle = win32gui.FindWindow(0, name)
    win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    win32gui.SetForegroundWindow(handle)

    if handle == 0:
        return

    x1, y1, x2, y2 = win32gui.GetWindowRect(handle)

    png = ImageGrab.grab((x1, y1, x2, y2))
    png.save(path)

    if isSaveWindowRect:
        Config.update('WindowRect', (x1, y1, x2, y2))


def is_zh_cn(text: str):
    """
     判断一个词是否是非英文词,只要包含一个中文，就认为是非英文词汇
    """
    count = 0
    for s in text.encode('utf-8').decode('utf-8'):
        if u'\u4e00' <= s <= u'\u9fff':
            count += 1
            break
    if count > 0:
        return True
    else:
        return False


def read_file(path):

    if not os.path.isfile(path):
        raise Exception("文件地址错误 {}", path)

    file = open(path, 'r',encoding='utf-8')
    try:
        return file.read()  # 结果为str类型
    finally:
        file.close()
