# Lokaverkefni - Guðmundur Óli og Helgi Steinarr - 11/21/2017
import threading
from PyQt5.QtCore import QDir, Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from time import sleep


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("mainwindow.ui", self)


class LoginWindow(QMainWindow):

    def __init__(self):
        super(LoginWindow, self).__init__()
        loadUi("loginwindow.ui", self)
        self.loginButton = self.findChild(QPushButton, "loginButton")
        self.loginButton.pressed.connect(self.login_button_clicked)

    def login_button_clicked(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
