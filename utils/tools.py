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
    print("鼠标点击事件：鼠标键位=", lOrR, "img=", img, "点击次数=", clickTimes, "重复次数=", reTry)
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


def application_screenshot_tool(name: str, path: str) -> None:
    """
    窗口截图工具
    :name 需要截图的窗口应用程序名称
    :path 截图保存的位置
    :isSaveWindowRect 是否需要将截图的窗口坐标保存下来
    """

    handle = window_top(name, True)

    if handle == 0:
        return

    png = ImageGrab.grab(Config.update('WindowRect'))
    png.save(get_join_pardir(path))


def window_top(name: str, isSaveWindowRect: bool = False):
    """
        窗口置顶
        :name:  窗口名称
        :return 窗口句柄
    """

    def callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            if win32gui.GetWindowText(hwnd) == name:
                extra[f"{name}"] = hwnd
                win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
                win32gui.SetForegroundWindow(hwnd)

    extra = {}
    win32gui.EnumWindows(callback, extra)

    if isSaveWindowRect:
        Config.update('WindowRect', win32gui.GetWindowRect(extra[name]))

    return extra[name]


def get_join_pardir(path: str):
    return os.path.join(os.path.abspath('..'), path)


def read_file(path):
    if not os.path.isfile(path):
        raise Exception("文件地址错误 {}", path)

    file = open(path, 'r', encoding='utf-8')
    try:
        return file.read()  # 结果为str类型
    finally:
        file.close()


def is_file(filename):
    return "\\" in filename and os.path.isfile(filename)
