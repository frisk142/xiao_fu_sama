import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
sys.stdout.reconfigure(encoding = "utf-8")

import os
import sys
import threading
import json
from PyQt5.QtCore import QUrl, QObject, pyqtSlot, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import Qt, pyqtSignal, QEvent
from xiao_fu_sama import chat_with_fu_jiang
from PyQt5.QtCore import pyqtSignal
from config.paths import INDEX_FILE, KEY_FILE
from config.api_key_manager import save_api_key, load_api_key


# 通信桥接
# 这里需要使用pyqt5的信号方式，子线程无法直接调用主线程的函数，所以需要要信号来传递数据，主线程接收到信号之后刷新ui
class Bridge(QObject):
    reply_signal = pyqtSignal(str) # 定义一个字符串类型的信号，用于传递回复内容
    def __init__(self,page):
        super().__init__()
        self.page = page
        self.reply_signal.connect(self.show_reply) # 将信号连接到显示回复的槽函数
        
    def show_reply(self, reply):
        safe_reply = json.dumps(reply)
        self.page.runJavaScript(f'document.getElementById("reply-box").innerText = {safe_reply}')
        print(reply)

    @pyqtSlot(str)
    def sendToPython(self, text):
        # 绑定api密钥命令
        if text.startswith("@bind"):
            key = text.replace("@bind", "").strip()
            if key:
                save_api_key(key)
                reply_save_key = "api密钥绑定成功，现在小芙可以正常聊天了\n如果需要更换密钥，请再次使用@bind命令绑定新的密钥.\n快开始你们的第一次聊天吧！"
                json.reply_save_key = json.dumps(reply_save_key)
                self.page.runJavaScript(f'document.getElementById("reply-box").innerText = {json.reply_save_key}')
                return
            
        api_key = load_api_key()
        print(f"当前API密钥: {api_key}")
        if not api_key:
            print("没有检测到api文件  not have api FILE")
            api_key_point = "请先绑定API密钥，格式：\n@bind YOUR_API_KEY\n如没有api密钥，请前往https://www.deepseek.com/中获取"
            json_api_key_point = json.dumps(api_key_point)
            self.page.runJavaScript(f'document.getElementById("reply-box").innerText = {json_api_key_point}')
            return

        # 聊天调用部分    
        print(f"[用户] {text}")

        def call():
            reply = chat_with_fu_jiang(text)
            self.reply_signal.emit(reply)
            print(reply)


        # 启动子线程
        threading.Thread(target=call, daemon=True).start()
    

# 定义桌宠窗口类 继承主窗口
class DesktopPet(QMainWindow):
    def __init__(self):
        super().__init__()
        # 设置窗口样式
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool ) #  | Qt.WindowTransparentForInput（鼠标穿透） 
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 500, 600)
        
        # 小芙的位置
        desktop = self.screen().availableGeometry()
        window_w = self.window().width()
        window_h = self.window().height()

        x = desktop.width() - window_w + 160
        y = desktop.height() - window_h + 170
        self.move(x , y)


        # 创建网络组件
        self.webview = QWebEngineView(self)
        self.webview.setGeometry(0, 0, 500, 600)
        self.webview.setAttribute(Qt.WA_TranslucentBackground)
        self.webview.page().setBackgroundColor(Qt.transparent) # 透明网页

        # 设置 WebChannel
        # 这段有意思，创建一个Bridge桥对象，然后把组件赋值于桥，让桥可以操控网页
        self.channel = QWebChannel()
        self.bridge = Bridge(self.webview.page()) # 创建通信桥对象
        self.bridge.view = self.webview # 把网络组件赋值给桥
        self.channel.registerObject("bridge", self.bridge) # 注册桥对象，js检索Bridge
        self.webview.page().setWebChannel(self.channel) # 绑定通信通道至网页

        # 加载 HTML
        self.webview.load(QUrl.fromLocalFile(INDEX_FILE))
        self.webview.show()

        # 窗口大小
        self.setFixedSize(320,420)

        # 拖拽条大小
        self.handle_width = 320
        self.handle_height = 10

        # 创建拖拽
        self.drag_handle = QFrame(self)
        self.drag_handle.setFixedSize(self.handle_width, self.handle_height)
        self.drag_handle.setStyleSheet("background: rgba(0,0,0,0.6); border-radius: 5px;") 
        self.drag_handle.raise_() # 确保漂浮最顶端
        
        # 初始化鼠标标记
        self.drag_pos =  None

        # 鼠标事件绑定
        self.drag_handle.mousePressEvent = self.handle_mouse_press
        self.drag_handle.mouseMoveEvent = self.handle_mouse_move
        self.drag_handle.mouseReleaseEvent = self.handle_mouse_release

    # 拖拽条样式
    def resizeEvent(self, event):
     margin = 40
     new_width = self.width() - 2 * margin
     if new_width < self.handle_width:
         new_width = 50
     self.drag_handle.setFixedWidth(new_width)
     x = (self.width() - new_width) // 2
     self.drag_handle.move(x, 2)
     super().resizeEvent(event)
     
    # 鼠标事件处理
    def handle_mouse_press(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos()

    def handle_mouse_move(self, event):
        if self.drag_pos:
            delta = event.globalPos() - self.drag_pos
            self.move(self.pos() + delta)
            self.drag_pos = event.globalPos()

    def handle_mouse_release(self, event):
        self.drag_pos = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DesktopPet()
    pet.show()
    sys.exit(app.exec_())