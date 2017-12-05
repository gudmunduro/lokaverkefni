from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

current = None

def show_date_picker(on_finish):
    global current
    current = DatePickerWindow(on_finish)
    current.show()

class DatePickerWindow(QMainWindow):

    def __init__(self, on_finish):
        super(DatePickerWindow, self).__init__()
        loadUi("datepicker.ui", self)
        self.cancel_button = self.findChild(QPushButton, "cancelButton")
        self.confirm_button = self.findChild(QPushButton, "confirmButton")
        self.calendar = self.findChild(QCalendarWidget, "calendarWidget")

        self.on_finish = on_finish

        self.cancel_button.pressed.connect(self.close)
        self.confirm_button.pressed.connect(self.on_confirm)

    def on_confirm(self):
        self.on_finish(self.calendar.selectedDate())
        self.close()
