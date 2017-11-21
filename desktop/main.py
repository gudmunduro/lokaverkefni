# Lokaverkefni - Guðmundur Óli og Helgi Steinarr - 11/21/2017
import threading
from PyQt5.QtCore import QDir, Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QCheckBox, QFileDialog, QGridLayout,
        QGroupBox, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpinBox,
QVBoxLayout, QWidget, QMainWindow, QProgressBar)
from PyQt5.uic import loadUi
from time import sleep


class Window(QWidget):

    def __init__(self):
        super(Window, self).__init__()

        self.button = QPushButton("Button")
        self.button.setFixedSize(60, 30)

        self.label = QLabel()
        self.label.setText("Lable")

        layout = QVBoxLayout()
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        layout.addWidget(self.button, alignment=Qt.AlignCenter)
        self.setLayout(layout)

        self.setWindowTitle("Window")
        self.resize(300, 200)

    def button_click(self):
        self.label.setText("Button clicked")


class WindoFromFile(QMainWindow):

    def __init__(self):
        super(QWidget, self).__init__()
        loadUi("mainwindow.ui", self)
        self.label = self.findChild(QLabel, "label")
        self.button = self.findChild(QPushButton, "pushButton")
        self.progress_bar = self.findChild(QProgressBar, "progressBar")

        self.button.clicked.connect(self.on_button_click)

    def on_button_click(self):
        self.label.setText("button clicked")
        t = threading.Thread(target=self.set_progress_bar())
        t.start()

    def set_progress_bar(self):
        value = 0
        self.progress_bar.setValue(0)
        while value < 100:
            value += 1
            self.progress_bar.setValue(value)
            sleep(0.01)

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = WindoFromFile()
    window.show()
    sys.exit(app.exec_())
