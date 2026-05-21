import sys
from pathlib import Path
import json
from Function.desktop_pet import DesktopPet
from PyQt5.QtWidgets import QApplication
from utils import resource_path

if __name__ == "__main__":
    app = QApplication(sys.argv)
    icon_path = resource_path("config/xiaofu_sama.ico")
    pet = DesktopPet()
    pet.show()
    sys.exit(app.exec_())