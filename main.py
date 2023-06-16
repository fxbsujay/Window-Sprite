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
