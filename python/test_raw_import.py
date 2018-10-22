from .gui.raw_import_window import Raw_Window
import sys
from PyQt5 import QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    interface = Raw_Window(window)
    window.show()

    sys.exit(app.exec_())