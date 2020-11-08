from PyQt5 import QtCore, QtWidgets, QtGui
import sys
from plotUI import MainWindow


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    app.exec_()


if __name__ == "__main__":
    # execute only if run as a script
    main()
