""""
# version:python 3.81
# -*- coding:utf-8 -*-

--------------------
# @Author       : fxbsujay@gmail.com
# @Time         : 11:39 2023/2/15
# @Version      : 1.0.0
# @Description  : 自动回复、聊天机器人
--------------------
"""
from ocr.orc_engine import OCRe
from utils.tools import *


class ReplySprite:
    pass


if __name__ == '__main__':
    OCRe.start()
    window_top('微信', True)

    location = pyautogui.locateCenterOnScreen(get_join_pardir('doc\\setting\\we_chat_flag.png'), confidence=0.8, region=Config.get('WindowRect'))

    we_chat_record_screenshot()
    text = OCRe.run(get_join_pardir(Config.get("screenshotSavePath")))
    print(text)
