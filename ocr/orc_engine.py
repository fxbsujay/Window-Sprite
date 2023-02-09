""""
# version:python 3.81
# -*- coding:utf-8 -*-

--------------------
# @Author       : fxbsujay@gmail.com
# @Time         : 10:44 2023/2/09
# @Version      : 1.0.0
# @Description  : Image OCR Engine
--------------------
"""

import os
from enum import Enum
from operator import eq
from ocr.api_image_ocr import OcrAPI
from utils.config import Config


class EngFlag(Enum):
    """引擎运行状态标志"""
    none = 0  # 不在运行
    initializing = 1  # 正在启动
    waiting = 2  # 待命
    running = 3  # 工作中


class OcrEngine:
    """OCR引擎，含各种操作的方法"""

    def __init__(self):
        self.__ocrInfo = ()  # 记录之前的OCR参数
        self.__ramTips = ''  # 内存占用提示
        self.ocr = None  # OCR API对象
        self.engFlag = EngFlag.none


    def __initVar(self):
        self.__ocrInfo = ()  # 记录之前的OCR参数
        self.__ramTips = ''  # 内存占用提示
        self.ocr = None  # OCR API对象


    def __setEngFlag(self, engFlag):
        """更新引擎状态"""

        self.engFlag = engFlag
        if self.ocr and Config.get('isDebug'):
            # 刷新内存占用
            if engFlag == EngFlag.waiting:
                self.__ramTips = f'（内存：{self.ocr.getRam()}）'

        msg = {
            EngFlag.none:  '已关闭',
            EngFlag.initializing:  '正在启动',
            EngFlag.waiting:  f'待命{self.__ramTips}',
            EngFlag.running:  f'工作{self.__ramTips}',
        }.get(engFlag, f'未知（{engFlag}）')

        Config.update('ocrProcessStatus', msg)


    def start(self):
        """启动引擎。若引擎已启动，且参数有更新，则重启。"""
        if self.engFlag == EngFlag.initializing:  # 正在初始化中，严禁重复初始化
            return

        ocrToolPath = Config.get('ocrToolPath')
        if not os.path.isfile(ocrToolPath):
            raise Exception(
                f'未在以下路径找到引擎组件\n【{ocrToolPath}】\n\n请将引擎组件【PaddleOCR-json】文件夹放置于指定路径！')

        # 获取静态参数
        ang = ' -cls=1 -use_angle_cls=1' if Config.get('isOcrAngle') else ''
        limit = f" -limit_type={Config.get('ocrLimitMode').get(Config.get('ocrLimitModeName'), 'min')} -limit_side_len={Config.get('ocrLimitSize')}"
        staticArgs = f"{ang}{limit}\
            -cpu_threads={Config.get('ocrCpuThreads')}\
            -enable_mkldnn={Config.get('isOcrMkldnn')}\
            {Config.get('argsStr')}"

        info = (
            Config.get("ocrToolPath"),
            Config.get('ocrConfig')[Config.get('ocrConfigName')]['path'],
            staticArgs
        )

        isUpdate = not eq(info, self.__ocrInfo)
        if self.ocr:
            if not isUpdate:
                return
            self.stop(True)

        self.__ocrInfo = info
        try:
            print('启动引擎，参数：{}',info)
            self.__setEngFlag(EngFlag.initializing)
            # 启动引擎
            self.ocr = OcrAPI(*self.__ocrInfo)
            # 检查启动引擎这段时间里，引擎有没有被叫停
            if not self.engFlag == EngFlag.initializing:
                # 状态被改变过了
                print(f'初始化后，引擎被叫停！{self.engFlag}')
                self.stop()
                return
            # 通知待命
            self.__setEngFlag(EngFlag.waiting)
        except Exception as e:
            self.stop()
            raise


    def stop(self, isRestart: bool = False):
        """立刻终止引擎。isRE为T时表示这是在重启"""

        if not self.engFlag == EngFlag.none and not isRestart:
            # TODO @CompilationTime 11:13 2023/02/09  --- 停止任务 ---
            print(f'引擎stop，停止任务！')

        if hasattr(self.ocr, 'stop'):
            self.ocr.stop()

        del self.ocr
        self.ocr = None
        self.__setEngFlag(EngFlag.none)
        self.__initVar()

    def run(self, path: str) -> dict:
        """执行单张图片识别，输入路径，返回字典"""

        if not self.ocr:
            self.__setEngFlag(EngFlag.none)  # 通知关闭
            return {'code': 404, 'data': f'引擎未在运行'}

        self.__setEngFlag(EngFlag.running)  # 通知工作
        data = self.ocr.run(path)

        if self.engFlag == EngFlag.running:
            self.__setEngFlag(EngFlag.waiting)  # 通知待命

        return data


OCRe = OcrEngine()




if __name__ == '__main__':
    orc = OCRe
    orc.start()
    text = orc.run("E:\\fxbsuajy@gmail.com\\Window-Sprite\\doc\\image\\screen.png")
    print(text)


