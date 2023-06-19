""""
# version:python 3.81
# -*- coding:utf-8 -*-

--------------------
# @Author       : fxbsujay@gmail.com
# @Time         : 18:00 2023/2/08
# @Version      : 1.0.0
# @Description  : System configuration information
--------------------
"""

from utils.enums import EngFlag, ScriptType

_ConfigDict = {
    # 启动参数字符串
    'argsStr': {
        'default': '',
    },
    # cls
    'isOcrAngle': {
        'default': False,
    },
    # 当前选择的压缩限制模式的name
    'ocrLimitModeName': {
        'default': '',
    },
    # 压缩限制模式
    'ocrLimitMode': {
        'default': {
            '长边压缩模式': 'max',
            '短边扩大模式': 'min',
        },
    },
    # 压缩阈值
    'ocrLimitSize': {
        'default': 960,
    },
    # CPU线程数
    'ocrCpuThreads': {
        'default': 10,
    },
    # 启用mkldnn加速
    'isOcrMkldnn': {
        'default': True,
    },
    # 进程运行状态字符串
    'ocrProcessStatus': {
        'default': EngFlag.none,
    },
    # 屏幕截图保存的位置
    'screenshotSavePath': {
        'default': 'doc\\screen.png',
    },
    # 脚本类型
    'taskScriptType': {
        'default': ScriptType.json,
    },
    'taskScriptPath': {
        'default': {
            'json': {
                'path': 'doc\\script.json'
            },
            'excel': {
                'path': 'doc\\script.xls'
            }
        }

    },
    # 过滤词组文件
    'banPhraseFilePath': {
        'default': "doc\\ban_phrase.txt"
    },
    # 窗体位置
    'WindowRect': {
        'default': None
    }

}


class ConfigModule:

    def __init__(self):
        self.__optDict = {}

        for key in _ConfigDict:
            value = _ConfigDict[key]
            self.__optDict[key] = value['default']

    def update(self, key, value):
        self.__optDict[key] = value

    def get(self, key):
        return self.__optDict[key]


Config = ConfigModule()