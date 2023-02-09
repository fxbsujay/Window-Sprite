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
from rich.console import Console

_ConfigDict = {

    # Debug模式
    'isDebug': {
        'default': False,
    },
    # 引擎路径
    'ocrToolPath': {
        'default': 'E:\\fxbsuajy@gmail.com\\Window-Sprite\\PaddleOCR-json\\PaddleOCR_json.exe',
    },
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
    'ocrConfig': {  # 配置文件信息
        'default': {  # 配置文件信息
            '简体中文': {
                'path': 'PaddleOCR_json_config_ch.txt'
            }
        },
    },
    # 当前选择的配置文件的name
    'ocrConfigName': {
        'default': '简体中文',
    },

    # 进程运行状态字符串
    'ocrProcessStatus': {
        'default': '未启动',
    },

    # 屏幕截图保存的位置
    'screenshotSavePath': {
        'default': 'doc/image/screen.png',
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


Config = ConfigModule()  # 设置模块 单例

console = Console()