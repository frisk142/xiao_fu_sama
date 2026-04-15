import tkinter as tk
from tkinter import scrolledtext
import threading
import ttkbootstrap as tb
from xiaofu_sama.xiao_fu_sama import chat_with_fu_jiang

class XiaofuGui:
    def __init__(self):
        self.window = tb.Window(themename = "minty")
        self.window.title("小芙酱")
        self.window.geometry("750x650")

        # self.window.iconbitmap("xiao_fu.ico")
        # 显示聊天区域
        self.chat_area = scrolledtext.ScrolledText(
            self.window,
            wrap = tk.WORD,
            font= ("微软雅黑",10),
            bg = "#F9F9F9",
            fg = "#333333",
            relief=tk.FLAT,
            insertbackground= "#E94F6F",
            borderwidth=0,
        )

        self.chat_area.pack(padx = 15 , pady = (15 , 10) , fill = tk.BOTH , expand=True) # 将文本框放入窗口
        self.chat_area.config(state = tk.DISABLED) # 只读

        # 消息标签样式
        self.chat_area.tag_config("user",foreground="#4A90E2",font=("微软雅黑",10))
        self.chat_area.tag_config("bot",foreground="#49f2b4",font=("微软雅黑",10))

        # 底部输入区域
        self.input_frame = tb.Frame(self.window)
        self.input_frame.pack(padx = 15, pady = (0,15), fill = tk.X)
        self.input_entry = tb.Entry(self.input_frame, font=("微软雅黑",10)) # 单行输入框
        self.input_entry.pack(side = tk.LEFT, fill = tk.X, expand = True, padx=(0,10)) # 放置框架左侧，水平填充
        self.input_entry.bind("<Return>",self.send_message) # 点击回车调用send_message模块
        self.send_btn = tb.Button(self.input_frame,text = "发送", command = self.send_message, bootstyle= "primary") # 在输入框放置发送按钮
        self.send_btn.pack(side = tk.RIGHT)

        # 欢迎语
        self.add_message("小芙酱","主人，我准备好啦，今天有什么可以帮助你的吗？", is_user = False)

        # 窗口循环
        self.window.mainloop()

        # 设置添加语句模块
    def add_message(self, sender, message, is_user = True):
        self.chat_area.config(state = tk.NORMAL)
        if is_user:
            self.chat_area.insert(tk.END,f"你:{message}\n","user")
        else:
            self.chat_area.insert(tk.END,f"{sender}:{message}\n","bot")
            self.chat_area.see(tk.END)
            self.chat_area.config(state=tk.DISABLED)

        # 设置发送消息模块
    def send_message(self, event = None):
        user_input = self.input_entry.get().strip()
        if not user_input:
            return
        self.add_message("你",user_input,is_user = True)
        self.input_entry.delete(0, tk.END)

        def call_bot():
            reply = chat_with_fu_jiang(user_input)
            self.window.after(0,self.add_message, "小芙酱", reply, False)

        threading.Thread(target=call_bot, daemon=True).start()

if __name__ == "__main__":
    XiaofuGui()










