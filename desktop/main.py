# Lokaverkefni - Guðmundur Óli og Helgi Steinarr - 11/21/2017
import threading
import json
import urllib.request, urllib.error
from PyQt5.QtCore import QDir, Qt, QTimer, QThread, QObject, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from time import sleep


# Main
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("mainwindow.ui", self)
        self.set_from_date_button = self.findChild(QPushButton, "setFromDateButton")
        self.set_to_date_button = self.findChild(QPushButton, "setToDateButton")

        self.set_from_date_button.pressed.connect(self.open_date_picker)
        self.set_to_date_button.pressed.connect(self.open_date_picker)

    def open_date_picker(self):
        self.date_picker_window = DatePickerWindow()
        self.date_picker_window.show()


class DatePickerWindow(QMainWindow):

    def __init__(self):
        super(DatePickerWindow, self).__init__()
        loadUi("datepicker.ui", self)
        self.cancel_button = self.findChild(QPushButton, "cancelButton")
        self.confirm_button = self.findChild(QPushButton, "confirmButton")

        self.cancel_button.pressed.connect(self.close)


# Login
class LoginWindow(QMainWindow):

    def __init__(self):
        super(LoginWindow, self).__init__()
        loadUi("loginwindow.ui", self)
        self.error_label = self.findChild(QLabel, "errorLabel")
        self.username_text_edit = self.findChild(QLineEdit, "usernameLineEdit")
        self.password_text_edit = self.findChild(QLineEdit, "passwordLineEdit")
        self.loginButton = self.findChild(QPushButton, "loginButton")

        self.loginButton.pressed.connect(self.login_button_clicked)
        self.password_text_edit.setEchoMode(QLineEdit.Password)
        self.error_label.setHidden(True)

        self.worker = CheckLoginWorkerObject(self)
        self.thread = QThread()
        self.worker.moveToThread(self.thread)

    def login_button_clicked(self):
        self.thread.start()
        self.worker.startWork()
        self.thread.start()

    def reset(self):
        self.username_text_edit.setText("")
        self.password_text_edit.setText("")
        self.error_label.setHidden(True)


class CheckLoginWorkerObject(QObject):

    def __init__(self, subclass, parent=None):
        super(self.__class__, self).__init__(parent)
        self.subclass = subclass

    @pyqtSlot()        
    def startWork(self):
        post_data = urllib.parse.urlencode({"username": self.subclass.username_text_edit.text(), "password": self.subclass.password_text_edit.text()})
        rq = urllib.request.Request('https://leiga.fisedush.com/api/admin/login', post_data.encode())
        data = urllib.request.urlopen(rq).read().decode()
        try:
            json_data = json.loads(data)
            if json_data["login_status"] == 1:
                self.main_window = MainWindow()
                self.main_window.show()
                self.subclass.close()
            else:
                self.subclass.error_label.setText("Villa: Notendanafn eða lykilorð er rangt")
                self.subclass.error_label.setHidden(False)
        except:
            self.subclass.error_label.setText("Óvent villa kom upp")
            self.subclass.error_label.setHidden(False)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
