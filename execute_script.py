""""
# version:python 3.81
# -*- coding:utf-8 -*-

--------------------
# @Author       : fxbsujay@gmail.com
# @Time         : 11:12 2023/2/07
# @Version      : 1.0.0
# @Description  : Automatic reply message robot execution script
--------------------
"""
from typing import List
from rich.table import Table
from utils.config import Config
from ocr.orc_engine import OCRe
from utils.config import console
from utils.tools import mouseClick, copy_image_to_clipboard, application_screenshot_tool
import pyperclip
import xlrd
import json
import pyautogui
import time
import os


def print_json_table(func):
    def _func(params: str):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("TYPE", style="dim")
        table.add_column("VALUE")
        table.add_column("RESET")
        console.rule("start scanning script")
        json_data = func(params)
        for item in json_data:
            table.add_row(str(item.type), str(item.value), str(item.reset))

        console.print(table)
        return json_data

    return _func


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


@print_json_table
def inspect_json(jsonStr: str) -> List[Script]:
    """
    :param jsonStr: json脚本
        For Example : [ { "type": 1, "value": "flag.png", "reset": 0} ]
    """
    jsonData: List[Script] = []
    if len(jsonStr) > 0:
        console.print_json(jsonStr)
        dataList = json.loads(jsonStr)
        for item in dataList:
            jsonData.append(Script(item['type'], item['value'], item['reset']))
    return jsonData


@print_json_table
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


class ExecuteScript:

    def __init__(self, loop: bool = True, filename: str = "doc//script.xls"):
        self._loop = loop
        self._filename = filename

        # 启动引擎
        OCRe.start()


    def execute_sheet_script(self) -> None:
        scriptData: List[Script] = inspect_sheet(self._filename)
        if self._loop:
            while True:
                self.execute_script(scriptData)
        else:
            self.execute_script(scriptData)

    def execute_json_script(self, jsonData: str = "") -> None:
        scriptData: List[Script] = inspect_json(jsonData)
        if self._loop:
            while True:
                self.execute_script(scriptData)
        else:
            self.execute_script(scriptData)


    @staticmethod
    def execute_script(dataList: List[Script]) -> None:
        console.rule("start execute script")
        for script in dataList:
            if script.type == 1.0 or script.type == 2.0:
                reset = 1
                if len(str(script.reset)) > 0:
                    reset = script.reset
                mouseClick(int(script.type), "left", script.value, reset)
            elif script.type == 3.0:
                reset = 1
                if len(str(script.reset)) > 0:
                    reset = script.reset
                mouseClick(1, "right", script.value, reset)
            elif script.type == 4.0:
                if os.path.isfile(script.value):
                    copy_image_to_clipboard(script.value)
                else:
                    pyperclip.copy(script.value)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.5)
            elif script.type == 5.0:
                waitTime = int(script.value)
                for i in range(waitTime):
                    application_screenshot_tool("企业微信")
                    text = OCRe.run(Config.get("screenshotSavePath"))
                    pyperclip.copy("你说的啥")
                    pyautogui.hotkey('ctrl', 'v')
                    time.sleep(1)

            elif script.type == 6.0:
                pyautogui.scroll(int(script.value))


if __name__ == '__main__':
    # inspect_json("[ { \"type\": 1, \"value\": \"flag.png\", \"reset\": 0} ]")
    execute = ExecuteScript()
    execute.execute_sheet_script()
