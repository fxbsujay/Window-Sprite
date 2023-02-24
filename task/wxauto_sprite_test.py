""""
# version:python 3.81
# -*- coding:utf-8 -*-

--------------------
# @Author       : fxbsujay@gmail.com
# @Time         : 11:39 2023/2/15
# @Version      : 1.0.0
# @Description  : 微信自动回复、聊天机器人
--------------------
"""
import json

from ocr.orc_engine import OCRe
from utils.tools import *


class ReplySprite:
    pass


if __name__ == '__main__':


    OCRe.start()
    window_top('微信', True)

    replyData = {}

    while True:
        location = pyautogui.locateCenterOnScreen(get_join_pardir('doc\\setting\\we_chat_flag.png'), confidence=0.8,
                                                  region=Config.get('WindowRect'))
        if location:
            pyautogui.click(location.x, location.y, clicks=1, interval=0.2, duration=0.2, button="left")
        get_we_chat_talk_name()
        replyName = OCRe.run(get_join_pardir("doc\\talk.png"))
        print(replyName)
        we_chat_record_screenshot()
        replyData[replyName[0]] = OCRe.run(get_join_pardir(Config.get("screenshotSavePath")))

        print(json.dumps(replyData, ensure_ascii=False))
