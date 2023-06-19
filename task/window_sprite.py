""""
# version:python 3.81
# -*- coding:utf-8 -*-

--------------------
# @Author       : fxbsujay@gmail.com
# @Time         : 11:12 2023/2/07
# @Version      : 1.0.0
# @Description  : 窗口自动化脚本 适用于 win11、win10
--------------------
"""
from threading import Thread
from typing import List
from ocr.orc_engine import OCRe
from utils.enums import EngFlag, ScriptType
from utils.tools import *
import pyperclip
import xlrd
import json
import pyautogui
import time
import os


class Script:
    """
        Script Model
    """

    def __init__(self, type: int, value: str, reset: int = 0):
        """
        :param type:    脚本类型
        :param value:   脚本内容
        """
        self._type = type
        self._value = value
        self._reset = reset

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value

    @property
    def reset(self):
        return self._reset

    def __str__(self):
        return 'type={},value={},reset={}'.format(self._type, self._value, self._reset)


def inspect_json(filename: str) -> List[Script]:
    """
    :param filename: json脚本文件
        For Example : [ { "type": 1, "value": "flag.png", "reset": 0} ]
    """
    jsonStr = read_file(filename)
    jsonData: List[Script] = []
    if len(jsonStr) > 0:
        dataList = json.loads(jsonStr)
        for item in dataList:
            jsonData.append(Script(item['type'], item['value'], item['reset']))
    return jsonData


def inspect_sheet(filename: str) -> List[Script]:
    """
        检测脚本并返回
        :param filename:  脚本文件路径
        :return: 脚本参数数组
    """
    wb = xlrd.open_workbook(filename=filename)
    sheet = wb.sheet_by_index(0)

    jsonData, index = [], 1
    if sheet.nrows < 2:
        return jsonData

    while index < sheet.nrows:
        scriptType = sheet.row(index)[0]

        if scriptType.ctype != 2 or (
                scriptType.value != 1.0 and scriptType.value != 2.0 and scriptType.value != 3.0
                and scriptType.value != 4.0 and scriptType.value != 5.0 and scriptType.value != 6.0):
            raise ValueError('第', index + 1, "行第一列数据格式不正确")
        else:
            scriptValue = sheet.row(index)[1]
            if scriptType.value == 1.0 or scriptType.value == 2.0 or scriptType.value == 3.0:
                if scriptValue.ctype != 1:
                    raise ValueError('第', index + 1, "行第二列数据格式不正确")
            elif scriptType.value == 4.0:
                if scriptValue.ctype == 0:
                    raise ValueError('第', index + 1, "行第二列数据格式不正确")
            elif scriptType.value == 5.0 or scriptType.value == 6.0:
                if scriptValue.ctype != 2:
                    raise ValueError('第', index + 1, "行第二列数据格式不正确")
            jsonData.append(Script(scriptType.value, scriptValue.value, sheet.row(index)[2].value))
        index += 1

    return jsonData


class WindowScript:

    def __init__(self, scriptType: ScriptType = ScriptType.json, loop: bool = True):
        """
            :param scriptType 脚本文件类型
            :loop  是否循环执行
        """
        self._loop = loop
        self._talk = None
        self._talkFlag = False

        if Config.get('taskScriptType'):
            scriptType = Config.get('taskScriptType')
        self._script = scriptType

        # 启动引擎
        if Config.get('ocrProcessStatus') == EngFlag.none:
            OCRe.start()


    def start(self) -> None:
        path = Config.get('taskScriptPath')[self._script.value]['path']
        filename = get_join_pardir(path)

        self._talkFlag = True
        scripts: List[Script] = inspect_sheet(filename) if self._script == ScriptType.excel else inspect_json(filename)

        def execute_talk():
            if not self._talkFlag:
                return
            if scripts and self._loop:
                while True:
                    self.execute_script(scripts)
            else:
                self.execute_script(scripts)

        if self._talk is None:
            self._talk = Thread(target=execute_talk, name="WindowScriptTalk")
            self._talk.daemon = True

        self._talk.start()


    def stop(self):
        if self._talkFlag:
            self._talkFlag = False


    @staticmethod
    def execute_script(dataList: List[Script]) -> None:
        print("start execute script")
        for script in dataList:
            if script.type == 1 or script.type == 2:
                reset = 1
                if len(str(script.reset)) > 0:
                    reset = script.reset
                mouseClick(int(script.type), "left", script.value, reset)
            elif script.type == 3:
                reset = 1
                if len(str(script.reset)) > 0:
                    reset = script.reset
                mouseClick(1, "right", script.value, reset)
            elif script.type == 4:
                if os.path.isfile(script.value):
                    copy_image_to_clipboard(script.value)
                else:
                    pyperclip.copy(script.value)
                pyautogui.hotkey('ctrl', 'v')
            elif script.type == 5:
                pyautogui.scroll(int(script.value))
            elif script.type == 6:
                time.sleep(int(script.value))


if __name__ == '__main__':
    # inspect_json("[ { \"type\": 1, \"value\": \"flag.png\", \"reset\": 0} ]")
    execute = WindowScript()
    execute.start()

