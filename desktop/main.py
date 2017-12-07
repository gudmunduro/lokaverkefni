# Lokaverkefni - Guðmundur Óli og Helgi Steinarr - 11/21/2017
import threading
import json
import urllib.request, urllib.error
from PyQt5.QtCore import QDir, Qt, QTimer, QThread, QObject, pyqtSlot, pyqtSignal, QDate
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from time import sleep
from requests_futures.sessions import FuturesSession
from datetime import datetime
from savedatamanager import LoginDataManager
from datepicker import show_date_picker


# Main
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("mainwindow.ui", self)
        self.set_from_date_button = self.findChild(QPushButton, "setFromDateButton")
        self.set_to_date_button = self.findChild(QPushButton, "setToDateButton")
        self.cars_table = self.findChild(QTableWidget, "carsTableWidget")

        self.set_from_date_button.pressed.connect(self.set_from_date_button_clicked)
        self.set_to_date_button.pressed.connect(self.set_to_date_button_clicked)

        date = datetime.now()
        self.set_from_date_button.setText(str(date.day) + "/" + str(date.month) + "/" + str(date.year))
        self.set_to_date_button.setText(str(date.day + 7) + "/" + str(date.month) + "/" + str(date.year))

        self.from_date = QDate(date.year, date.month, date.day)
        self.to_date = QDate(date.year, date.month, date.day + 7)

        self.update_day_count_label()

        self.car_rq_test()

    def set_from_date_button_clicked(self):
        def on_finish(date):
            last_date = self.from_date
            self.from_date = date
            self.set_from_date_button.setText(str(date.day()) + "/" + str(date.month()) + "/" + str(date.year()))
            if self.day_count < 1:
                QMessageBox.about(self, "Villa", "Dagarnir geta ekki verið færri en einn")
                self.from_date = last_date
                self.set_from_date_button.setText(str(self.to_date.day()) + "/" + str(self.to_date.month())
                                                + "/" + str(self.to_date.year()))
            self.update_day_count_label()
            print(self.from_date.toString())
            print(self.to_date.toString())
        show_date_picker(on_finish)

    def set_to_date_button_clicked(self):
        def on_finish(date):
            last_date = self.to_date
            self.to_date = date
            self.set_to_date_button.setText(str(date.day()) + "/" + str(date.month()) + "/" + str(date.year()))
            if self.day_count < 1:
                QMessageBox.about(self, "Villa", "Dagarnir geta ekki verið færri en einn")
                self.to_date = last_date
                self.set_to_date_button.setText(str(self.to_date.day()) + "/" + str(self.to_date.month())
                                                + "/" + str(self.to_date.year()))
            self.update_day_count_label()
        show_date_picker(on_finish)

    @property
    def day_count(self):
        count = (self.to_date.day() - self.from_date.day())
        return (count if count != 0 else 1)

    def update_day_count_label(self):
        day_count_label = self.findChild(QLabel, "dayCountLabel")
        day_count_label.setText(str(self.day_count))

    def car_rq_test(self):
        session = FuturesSession()

        rq = session.get("https://leiga.fisedush.com/api/cars", background_callback=self.on_load)

    def on_load(self, session, response):
        cars = response.json()
        for car in cars:
            row_count = self.cars_table.rowCount()
            self.cars_table.insertRow(row_count)
            self.cars_table.setItem(row_count, 0, QTableWidgetItem(str(car[0])))
            self.cars_table.setItem(row_count, 1, QTableWidgetItem(str(car[1])))
            self.cars_table.setItem(row_count, 2, QTableWidgetItem(str(car[2])))
            self.cars_table.setItem(row_count, 3, QTableWidgetItem(str(car[3])))
            self.cars_table.setItem(row_count, 4, QTableWidgetItem(str(car[4])))
            self.cars_table.setItem(row_count, 5, QTableWidgetItem(str(car[5])))
            self.cars_table.setItem(row_count, 6, QTableWidgetItem(str(car[6])))
            self.cars_table.setItem(row_count, 7, QTableWidgetItem(str(car[7])))
            self.cars_table.setItem(row_count, 8, QTableWidgetItem(str(car[11])))
            self.cars_table.setItem(row_count, 9, QTableWidgetItem(str(car[8])))
            self.cars_table.setColumnCount(10)


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

        login_data_manager = LoginDataManager()
        if login_data_manager.user_info_saved:
            self.username_text_edit.setText(login_data_manager.username)
            self.password_text_edit.setText(login_data_manager.password)
            self.save_login_info_check_box.setChecked(True)

    def login_button_clicked(self):
        self.temp_login()
        return
        session = FuturesSession()

        self.open_window = pyqtSignal(object)
        self.open_window.connect(self.open_main_window)

        post_data = "username=" + self.username_text_edit.text() + "&password=" + self.password_text_edit.text()
        rq = session.post("https://leiga.fisedush.com/api/admin/login", data=post_data,
                          background_callback=self.on_login_rq_complete)

    def on_login_rq_complete(self, session, response):
        data = response.json()
        try:
            if data["login_status"] == 1:
                if self.save_login_info_check_box.isChecked():
                    login_data_manager = LoginDataManager()
                    login_data_manager.username = self.username_text_edit.text()
                    login_data_manager.password = self.password_text_edit.text()
                self.open_window.emit()
            else:
                self.error_label.setText("Villa: Notendanafn eða lykilorð er rangt")
                self.error_label.setHidden(False)
        except:
            self.error_label.setText("Óvent villa kom upp")
            self.error_label.setHidden(False)

    def temp_login(self):
        post_data = urllib.parse.urlencode({"username": self.username_text_edit.text(),
                                            "password": self.password_text_edit.text()})
        rq = urllib.request.Request('https://leiga.fisedush.com/api/admin/login', post_data.encode())
        data = urllib.request.urlopen(rq).read().decode()
        try:
            json_data = json.loads(data)
            if json_data["login_status"] == 1:
                if self.save_login_info_check_box.isChecked():
                    login_data_manager = LoginDataManager()
                    login_data_manager.username = self.username_text_edit.text()
                    login_data_manager.password = self.password_text_edit.text()
                self.open_main_window()
            else:
                self.error_label.setText("Villa: Notendanafn eða lykilorð er rangt")
                self.error_label.setHidden(False)
        except:
            self.error_label.setText("Óvent villa kom upp")
            self.error_label.setHidden(False)

    def open_main_window(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.hide()

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
