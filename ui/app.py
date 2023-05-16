import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter.scrolledtext import ScrolledText
from threading import Thread
from utils.config import Config
from utils.config import console
from utils.enums import PurposeType, EngFlag
import time


class FileSearchEngine(ttk.Frame):

    def __init__(self, master, statusChangeHandle=None):
        super().__init__(master, padding=15)
        self.pack(fill=BOTH, expand=YES)

        self._statusChangeHandle = statusChangeHandle
        self._status_var = ttk.StringVar(value='启动')

        self._option_lf = ttk.Labelframe(self, text="操作", padding=15)
        self._option_lf.pack(fill=X, expand=YES, anchor=N)

        self.create_operation_row()
        self.create_log_row()

    def create_operation_row(self):
        path_row = ttk.Frame(self._option_lf)
        path_row.pack(fill=X, expand=YES)

        contains_opt = ttk.Radiobutton(
            master=path_row,
            text=PurposeType.daily.value,
            value=PurposeType.daily
        )
        contains_opt.pack(side=LEFT)

        startswith_opt = ttk.Radiobutton(
            master=path_row,
            text=PurposeType.weChat.value,
            value=PurposeType.weChat
        )
        startswith_opt.pack(side=LEFT, padx=15)

        status_btn = ttk.Button(
            master=path_row,
            textvariable=self._status_var,
            command=self.status_bnt_click_handle,
            width=8
        )
        status_btn.pack(side=LEFT, padx=5)

    # 日志显示框
    def create_log_row(self):
        style = ttk.Style()
        self.textbox = ScrolledText(
            master=self,
            highlightcolor=style.colors.primary,
            highlightbackground=style.colors.border,
            highlightthickness=1
        )
        self.textbox.pack(fill=X, expand=YES, pady=15)
        default_txt = "Click the browse button to open a new text file."
        self.textbox.insert(END, default_txt)

        t = Thread(target=self.open_log)
        t.daemon = True
        t.start()

    def open_log(self):
        while True:
            with open('log.txt', encoding='utf-8') as f:
                self.textbox.delete('1.0', END)
                self.textbox.insert(END, f.readlines())
                time.sleep(1)
                console.print('22222')
                f.close()

    def status_bnt_click_handle(self):

        if self._statusChangeHandle:
            self._statusChangeHandle()

        status_describe = {
            EngFlag.none: '启动',
            EngFlag.initializing: '正在启动',
            EngFlag.waiting: '停止',
            EngFlag.running: '停止'
        }

        status = Config.get('ocrProcessStatus')
        self._status_var.set(status_describe[status])


def start():
    Config.update('ocrProcessStatus', EngFlag.waiting)


if __name__ == '__main__':
    app = ttk.Window("File Search Engine")

    console.print('aaaa')
    engine = FileSearchEngine(app, start)
    app.mainloop()

