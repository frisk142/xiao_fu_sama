import tkinter as tk
from tkinter import scrolledtext
import threading
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from xiaofu_sama.xiao_fu_sama import chat_with_fu_jiang

class XiaofuGui:
    def __init__(self):
        self.window = tb.Window(themename = "minty")
        self.window.title("小芙酱")
        self.window.geometry("600x400")
        self.window.resizable(width=False, height=False)

        # self.window.iconbitmap("xiao_fu.ico")

        # 显示聊天区域
        self.chat_area = scrolledtext.ScrolledText(
            self.window,
            wrap = tk.WORD,
            font= ("微软雅黑",10),
            bg = "#F9F9F9",
            fg = "#333333",
            relief=tk.FLAT,
            borderwidth=0,
        )
        self.chat_area.pack(padx = 15 , pady = (15 , 10) , fill = tk.BOTH , expand=True)
        self.chat_area.config(state = tk.DISABLED)

        # 消息标签样式
        self.chat_area.tag_config("user",foreground="#4A90E2",font=("微软雅黑",10))
        self.chat_area.tag_config("bot",foreground="#E94F6F",font=("微软雅黑",10))

        # 底部输入区域
        self.input_frame = tb.Frame(self.window)
        self.input_frame.pack(padx = 15, pady = (0,15), fill = tk.x)
        self.input_entry = tb.Entry(self.input_frame, font=("微软雅黑",10))
        self.input_entry.pack(size = tk.LEFT, fill = tk.x, expand = True, padx=(0,10))
        self.send_btn = tb.Button(self.input_frame,text = "发送", command = self.send_message, bootstyle= "primary")
        self.send_btn.pack(side = tk.RIGHT)







