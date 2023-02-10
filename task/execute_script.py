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
from ocr.orc_engine import OCRe
from utils.enums import EngFlag, ScriptType
from utils.tools import *
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
def inspect_json(filename: str) -> List[Script]:
    """
    :param filename: json脚本文件
        For Example : [ { "type": 1, "value": "flag.png", "reset": 0} ]
    """
    jsonStr = read_file(filename)
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
                if scriptValue.ctype != 1:
                    raise ValueError('第', index + 1, "行第二列数据格式不正确")
            jsonData.append(Script(scriptType.value, scriptValue.value, sheet.row(index)[2].value))
        index += 1

    return jsonData


class ExecuteScript:

    def __init__(self, scriptType: ScriptType = ScriptType.json, loop: bool = True, isBanPhrases: bool = True):
        self._phrases = []
        self._loop = loop

        if Config.get('taskScriptType'):
            scriptType = Config.get('taskScriptType')
        self._script = scriptType

        # 启动引擎
        if Config.get('ocrProcessStatus') == EngFlag.none:
            OCRe.start()

        if isBanPhrases:
            self.filter_phrases()

    def filter_phrases(self):
        path = get_join_pardir(Config.get("banPhraseFilePath"))
        if path:
            content = read_file(path)
            if content:
                self._phrases = content.split(',')

    def start(self) -> None:
        path = Config.get('taskScriptPath')[self._script.value]['path']
        filename = get_join_pardir(path)

        scriptData: List[Script] = []

        if self._script == ScriptType.excel:
            scriptData = inspect_sheet(filename)
        elif self._script == ScriptType.json:
            scriptData = inspect_json(filename)

        if scriptData and self._loop:
            while True:
                self.execute_script(scriptData, self._phrases)
        else:
            self.execute_script(scriptData, self._phrases)


    @staticmethod
    def execute_script(dataList: List[Script], banPhrases: []) -> None:
        console.rule("start execute script")
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
                screenshotSavePath = get_join_pardir(Config.get("screenshotSavePath"))
                application_screenshot_tool(script.value, screenshotSavePath, isSaveWindowRect=True)
                text = OCRe.run(screenshotSavePath)
                console.print(text)
                entries = [item for item in list(set(text)) if item not in banPhrases and is_zh_cn(item)]

                pyperclip.copy("您好，我是机器人 MOSS")
                pyautogui.hotkey('ctrl', 'v')

            elif script.type == 6:
                pyautogui.scroll(int(script.value))



if __name__ == '__main__':
    # inspect_json("[ { \"type\": 1, \"value\": \"flag.png\", \"reset\": 0} ]")
    execute = ExecuteScript()
    execute.start()
