import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt5应用程序")
        self.setGeometry(100, 100, 400, 200)

        self.label = QLabel(self)
        self.label.setText("欢迎使用PyQt5！")
        self.label.move(100, 80)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
