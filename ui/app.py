import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter.scrolledtext import ScrolledText
from utils.config import console
from threading import Thread
import time


class FileSearchEngine(ttk.Frame):

    def __init__(self, master, startAndEndFunc):
        super().__init__(master, padding=15)
        self.pack(fill=BOTH, expand=YES)

        self.option_lf = ttk.Labelframe(self, text="操作", padding=15)
        self.option_lf.pack(fill=X, expand=YES, anchor=N)


        self._startAndEndFunc = startAndEndFunc

        self.create_operation_row()
        self.create_log_row()




    def create_operation_row(self):
        path_row = ttk.Frame(self.option_lf)
        path_row.pack(fill=X, expand=YES)
        browse_btn = ttk.Button(
            master=path_row,
            text="启动",
            command=self._startAndEndFunc,
            width=8
        )
        browse_btn.pack(side=LEFT, padx=5)

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
        t.start()


    def open_log(self):
        while True:
            with open('log.txt', encoding='utf-8') as f:
                self.textbox.delete('1.0', END)
                self.textbox.insert(END, f.read())
                time.sleep(1)
                f.close()


def aafr():
    pass


if __name__ == '__main__':


    app = ttk.Window("File Search Engine")
    FileSearchEngine(app, None)
    app.mainloop()
