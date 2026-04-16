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


class Bridge(QObject):
    """JS 与 Python 通信桥接"""
    @pyqtSlot(str)
    def sendToPython(self, text):
        print(f"[用户] {text}")
        def call():
            reply = chat_with_fu_jiang(text)
            print(reply)
            # 在主线程中执行 JS 显示回复
            QTimer.singleShot(0, lambda: self.view.page().runJavaScript(f"window.showMessage('{reply}', 5000)"))
        threading.Thread(target=call, daemon=True).start()

class DesktopPet(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 500, 600)

        self.webview = QWebEngineView(self)
        self.webview.setGeometry(0, 0, 500, 600)
        self.webview.setAttribute(Qt.WA_TranslucentBackground)
        self.webview.page().setBackgroundColor(Qt.transparent)

        # 设置 WebChannel
        self.channel = QWebChannel()
        self.bridge = Bridge()
        self.bridge.view = self.webview
        self.channel.registerObject("bridge", self.bridge)
        self.webview.page().setWebChannel(self.channel)

        # 加载 HTML
        self.webview.load(QUrl.fromLocalFile(index_file))
        self.webview.show()

        # 实现窗口拖拽
        self.drag_pos = None
        self.webview.mousePressEvent = self.mousePressEvent
        self.webview.mouseMoveEvent = self.mouseMoveEvent
        self.webview.mouseReleaseEvent = self.mouseReleaseEvent

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