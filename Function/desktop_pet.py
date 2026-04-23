import sys
import threading
from PyQt5.QtCore import QUrl, QObject, pyqtSlot, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import Qt
from xiaofu_sama.xiao_fu_sama import chat_with_fu_jiang
import os

bate_dir = os.path.dirname(__file__)
index_file = os.path.join(bate_dir, "index.html")


# 通信桥接
class Bridge(QObject):
    def show_reply(self, reply):
        self.view.page().runJavaScript(f'''
            document.getElementById('reply-box').innerText = `{reply}`
        ''')

    @pyqtSlot(str)
    def sendToPython(self, text):
        print(f"[用户] {text}")

        def call():
            reply = chat_with_fu_jiang(text)
            print(f"小芙酱：{reply}")
            print(len(reply))

            QTimer.singleShot(0, lambda: self.show_reply(reply))

        # 启动子线程
        threading.Thread(target=call, daemon=True).start()

# 定义桌宠窗口类 继承主窗口
class DesktopPet(QMainWindow):
    def __init__(self):
        super().__init__()
        # 设置窗口样式
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 500, 600)

        # 创建网络组件
        self.webview = QWebEngineView(self)
        self.webview.setGeometry(0, 0, 500, 600)
        self.webview.setAttribute(Qt.WA_TranslucentBackground)
        self.webview.page().setBackgroundColor(Qt.transparent) # 透明网页

        # 设置 WebChannel
        # 这段有意思，创建一个Bridge桥对象，然后把组件赋值于桥，让桥可以操控网页
        self.channel = QWebChannel()
        self.bridge = Bridge() # 创建通信桥对象
        self.bridge.view = self.webview # 把网络组件赋值给桥
        self.channel.registerObject("bridge", self.bridge) # 注册桥对象，js检索Bridge
        self.webview.page().setWebChannel(self.channel) # 绑定通信通道至网页

        # 加载 HTML
        self.webview.load(QUrl.fromLocalFile(index_file))
        self.webview.show()

        # 实现窗口拖拽
        self.drag_pos = None
        self.webview.mousePressEvent = self.mousePressEvent
        self.webview.mouseMoveEvent = self.mouseMoveEvent
        self.webview.mouseReleaseEvent = self.mouseReleaseEvent

    # 与窗口拖拽有关，但未能整理
    def mousePressEvent(self, event):
        self.drag_pos = event.globalPos()
    def mouseMoveEvent(self, event):
        if self.drag_pos:
            delta = event.globalPos() - self.drag_pos
            self.move(self.pos() + delta)
            self.drag_pos = event.globalPos()
    def mouseReleaseEvent(self, event):
        self.drag_pos = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DesktopPet()
    pet.show()
    sys.exit(app.exec_())