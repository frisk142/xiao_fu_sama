import tkinter as tk
from tkinter import scrolledtext
import threading
from xiaofu_sama.xiao_fu_sama import chat_with_fu_jiang

class Xoao_fu_Gui :
    def __init__(self):
        # 创建主要窗口
        self.window = tk.Tk()
        self.window.title("xiao_fu") # 窗口标题
        self.window.geometry("500x600") # 宽高
        self.window.configure(bg = "white")

        # 聊天显示
        self.chat_fujiang = scrolledtext.ScrolledText(
            self.window,
            wrap = tk.WORD, 
            width = 60,
            height = 25,
            font = ("AcadEref",10),
            bg = "white",
            fg = "black",
        )

        self.chat_fujiang.pack(padx = 10 ,pady = 10 , fill = tk.BOTH, expand = True)
        self.chat_fujiang.config(state = tk.DISABLED) # 只读

        # 底部输入
        self.input_frame = tk.Frame(self.window , bg = "white") # self.window??
        self.input_frame.pack(padx=10, pady=5, fill=tk.X)

        # 输入框
        self.input_entry = tk.Entry(self.input_frame, font=("AcadEref", 10))
        self.input_entry.pack(side = tk.LEFT,fill = tk.X , expand = True , padx = (0 , 5))

        # 回车键发送
        self.input_entry.bind("<Return>",self.send_message)

        # 发送按钮
        self.send_btn = tk.Button(self.input_frame , text = "发送" , command = self.send_message)
        self.send_btn.pack(side = tk.RIGHT)

        # 欢迎语
        self.add_message("小芙酱","准备好啦~✨今天有什么想要做的吗？" , is_user = False)

        # 启动窗口主循环
        self.window.mainloop()

        # 在聊天区域显示消息
    def add_message(self,sender,text,is_user = True):
        self.chat_fujiang.config(state = tk.NORMAL) # 临时解锁编辑，方便测试
        if is_user:
            self.chat_fujiang.insert(tk.END,f"你{text}\n","user")
        else:
            self.chat_fujiang.insert(tk.END,f"{sender}:{text}\n","bot")
            self.chat_fujiang.see(tk.END)  # 页面自动滚动到底部
            self.chat_fujiang.config(state = tk.DISABLED)   # 锁定位置

            # 设置不同角色的字体。颜色
            self.chat_fujiang.tag_config("user" , foreground="blue" , font=("AcadEref" , 10))
            self.chat_fujiang.tag_config("bot" , foreground="blue", font=("AcadEref", 10))

        # 处理用户发送的消息
    def send_message(self,event = None):
        user_input = self.input_entry.get().strip() # 挂个strip 清一下特殊符号（可选删？）
        if not user_input:
            return

        self.add_message("你：",user_input, is_user = False) # 显示用户消息
        self.input_entry.delete(0, tk.END)  # 发送消息之后清空输入框

        # 在新线程中调用小芙酱，避免界面卡死
        def call_bot():
            reply = chat_with_fu_jiang(user_input)
            self.window.after(0, self.add_message, "小芙酱", reply, False)

        threading.Thread(target=call_bot, daemon=True).start()

if __name__ == "__main__":
    Xoao_fu_Gui()


























