# 自动化办公 解放双手

---
- pip install pyperclip          (电脑剪切板库)
- pip install xlrd               (excel操作库)  
- pip install pyautogui==0.9.50  (鼠标键盘操作库)
- pip install pillow        (图片操作库)  
- pip install rich          (打印，日志输出  )
- pip install pywin32       (Windows api)  
- pip install pytesseract   (图像识别库)
- pip install psutil        (系统监控)
- pip install pyinstaller   (打包程序)
- pip install opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple  
```
安装 doc文件夹内的 tesseract.exe  
将 chi_sim 文件放入 tesseract的安装路径\\tesseract\\tesseract内  
找到 pytesseract.py文件的第28行改为以下路径 
tesseract_cmd = 'tesseract的安装路径\\tesseract\\tesseract'
```