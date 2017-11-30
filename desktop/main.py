# Lokaverkefni - Guðmundur Óli og Helgi Steinarr - 11/21/2017
import threading
import json
import grequests
import urllib.request, urllib.error
from PyQt5.QtCore import QDir, Qt, QTimer, QThread, QObject, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from time import sleep
from savedatamanager import LoginDataManager


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
        self.login_button = self.findChild(QPushButton, "loginButton")
        self.save_login_info_check_box = self.findChild(QCheckBox, "saveLoginInfoCheckBox")

        self.login_button.pressed.connect(self.login_button_clicked)
        self.password_text_edit.setEchoMode(QLineEdit.Password)
        self.error_label.setHidden(True)

        self.worker = CheckLoginWorkerObject(self)
        self.thread = QThread()
        self.worker.moveToThread(self.thread)

        login_data_manager = LoginDataManager()
        if login_data_manager.user_info_saved:
            self.username_text_edit.setText(login_data_manager.username)
            self.password_text_edit.setText(login_data_manager.password)
            self.save_login_info_check_box.setChecked(True)

    def login_button_clicked(self):
        self.thread.start()
        self.worker.check_login()

    def reset(self):
        self.username_text_edit.setText("")
        self.password_text_edit.setText("")
        self.error_label.setHidden(True)


class CheckLoginWorkerObject(QObject):

    def __init__(self, login_window, parent=None):
        super(self.__class__, self).__init__(parent)
        self.login_window = login_window

    @pyqtSlot()
    def check_login(self):
        post_data = urllib.parse.urlencode({"username": self.login_window.username_text_edit.text(), "password": self.login_window.password_text_edit.text()})
        rq = urllib.request.Request('https://leiga.fisedush.com/api/admin/login', post_data.encode())
        data = urllib.request.urlopen(rq).read().decode()
        try:
            json_data = json.loads(data)
            if json_data["login_status"] == 1:
                if self.login_window.save_login_info_check_box.isChecked():
                    login_data_manager = LoginDataManager()
                    login_data_manager.username = self.login_window.username_text_edit.text()
                    login_data_manager.password = self.login_window.password_text_edit.text()
                self.main_window = MainWindow()
                self.main_window.show()
                self.login_window.close()
            else:
                self.login_window.error_label.setText("Villa: Notendanafn eða lykilorð er rangt")
                self.login_window.error_label.setHidden(False)
        except:
            self.login_window.error_label.setText("Óvent villa kom upp")
            self.login_window.error_label.setHidden(False)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
