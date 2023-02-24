import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import ttkbootstrap.dialogs as ttkdialog
import tkinter.messagebox as tkmessage

win = ttk.Window(resizable=(False, False))
win.title('文本编辑器')

frame = ttk.Frame(win, )
frame.pack()
filename = ttk.StringVar()
entry_file = ttk.Entry(frame, textvariable=filename)


def browse():
    try:
        path = askopenfilename()
        if not path:
            return

        with open(path, encoding='utf-8') as f:
            text.delete('1.0', ttk.END)
            text.insert(ttk.END, f.read())
            filename.set(path)
    except UnicodeDecodeError:
        ttkdialog.Messagebox.show_error('编码错误')


def save():
    try:
        content = text.get(0.0, ttk.END)
        file_path = entry_file.get()

        if entry_file.get() == "":
            file_path = asksaveasfilename(title="保存：请注意输入后缀名")
            filename.set(file_path)
            with open(file_path, 'a') as f:
                f.write(content)
        with open(file_path, 'w') as fw:
            fw.write(content)
    except:
        pass


def about():
    ttkdialog.Messagebox.show_info('作者：UPaixi 于2023-1-16', '关于')


def new():
    try:
        entry_file.delete(0, ttk.END)
        text.delete(0.0, ttk.END)
        ttkdialog.Messagebox.show_info('新建成功', '完成')

    except:
        ttkdialog.Messagebox.show_error('新建失败', '错误')


def if_closing():
    close = tkmessage.askyesno("关闭", "确定关闭吗？请注意文件保存")
    if close == True:
        win.destroy()
    else:
        pass

if __name__ == '__main__':
    text = ttk.ScrolledText(frame)
    text.pack(padx=(5, 5), pady=10)

    menubar = ttk.Menu(frame)
    menus = ttk.Menu(menubar)

    menubar.add_cascade(label="文件", menu=menus)
    menubar.add_cascade(label="关于", command=about)

    menus.add_command(label="新建", command=new)
    menus.add_command(label="保存", command=save)
    menus.add_command(label="打开", command=browse)

    menus.add_separator()

    menus.add_command(label="退出", command=if_closing)

    win.protocol('WM_DELETE_WINDOW', if_closing)
    win.config(menu=menubar)

    win.mainloop()