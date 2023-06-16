# 微信客户端自动化

|  环境  |                             版本                             |
| :----: | :----------------------------------------------------------: |
|   OS   | [![Windows](https://img.shields.io/badge/Windows-10-white?logo=windows&logoColor=white)](https://www.microsoft.com/) |
|  微信  | [![Wechat](https://img.shields.io/badge/%E5%BE%AE%E4%BF%A1-3.9.5.81-07c160?logo=wechat&logoColor=white)](https://weixin.qq.com/cgi-bin/readtemplate?ang=zh_CN&t=page/faq/win/335/index&faq=win_335) |
| Python | [![Python](https://img.shields.io/badge/Python-3.81-blue?logo=python&logoColor=white)](https://www.python.org/) |

已实现发送微信消息，发送文件，获取微信聊天记录等功能

## Example:

------

```python
from task.wx_api import WeChat

if __name__ == '__main__':
    wx = WeChat()

    # 获取当前微信窗口所展示的所有会话
    for session in wx.refresh_sessions():
        print(session)

    # 打开聊天窗
    wx.open_session("文件传输助手")

    # 搜索某个会话
    wx.search_session("文件传输助手")

    # 获取所有有未读消息的用户
    for unreadUser in wx.get_unread_message_users():
        print(unreadUser)

    # 查询所有当前窗口的聊天消息
    for message in wx.get_all_message():
        print(str(message))

    # 获取最后一条消息
    print(wx.get_last_message())

    # 向当前聊天窗口发送文消息
    wx.send_message("Hello World")

    # 向当前聊天窗口发送文件
    wx.send_file("C:\Program Files\\readme.md")
```

