import pytesseract
import win32con, win32gui
from PIL import ImageGrab, Image
import os
import time



def get_window_pos(name):
    name = name
    handle = win32gui.FindWindow(0, name)
    win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    win32gui.SetForegroundWindow(handle)
    if handle == 0:
        return None
    else:
        return win32gui.GetWindowRect(handle)


if __name__ == '__main__':
    x1, y1, x2, y2 = get_window_pos('企业微信')

    png = ImageGrab.grab((x1, y1, x2, y2))
    png.save('doc/image/screen.png')

    text = pytesseract.image_to_string(Image.open("doc/image/screen.png"), lang='chi_sim')
    print(text)
