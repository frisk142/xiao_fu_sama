import tkinter as tk
from tkinter import scrolledtext
import threading
from xiaofu_sama.xiao_fu_sama import chat_with_fu_jiang

class Xoao_fu_Gui :
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("xiao_fu") # 窗口标题
        self.window.geometry("500x600") # 宽高
        self.window.configure(bg = "white")
