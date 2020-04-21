from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QDialog
from PyQt5.QtCore import QTime
from countdown import CountdownThread

import PyQt5.QtMultimedia as M
import time


class IntervalTimerGui(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.counter = 0
        self.time_left = 7200 # 2h
        self.time = QTime(0, 0, 0) # h m s ms
        self.setup_UI()
    

    def setup_UI(self):
        wid = QWidget()
        self.time = self.time.addSecs(self.time_left)
        self.time_label = QLabel(self.time.toString())
        self.time_descr_label = QLabel("Time")
        self.counter_descr_label = QLabel("Counter:")
        self.counter_label = QLabel(str(self.counter))
        
        self.start_stop_btn = QPushButton("Start")
        self.start_stop_btn.clicked.connect(self.pressed_start)
        self.done_btn = QPushButton("Done")
        self.done_btn.setEnabled(False)
        self.done_btn.clicked.connect(self.pressed_done)

        hbox_1 = QHBoxLayout()
        hbox_1.addWidget(self.time_descr_label)
        hbox_1.addWidget(self.time_label)
        hbox_1.addWidget(self.start_stop_btn)

        hbox_2 = QHBoxLayout()
        hbox_2.addWidget(self.counter_descr_label)
        hbox_2.addWidget(self.counter_label)
        hbox_2.addWidget(self.done_btn)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_1)
        vbox.addLayout(hbox_2)
        wid.setLayout(vbox)
        self.setCentralWidget(wid)

        title = "Interval Timer"
        self.setWindowTitle(title)


    def pressed_start(self):
        self.start_stop_btn.disconnect()
        self.start_stop_btn.setText("Stop")
        self.start_stop_btn.clicked.connect(self.pressed_stop)
        self.count_down()


    def pressed_stop(self):
        self.start_stop_btn.disconnect()
        self.start_stop_btn.setText("Start")
        self.start_stop_btn.clicked.connect(self.pressed_start)
        self.worker.stop()


    def pressed_done(self):
        self.done_btn.setEnabled(False)
        self.counter += 1
        self.counter_label.setText(str(self.counter))
        self.start_stop_btn.setEnabled(True)
        self.pressed_stop()
        self.reset_timer()



    def reset_timer(self):
        self.time = QTime(0, 0, 0)
        self.time_left = 7200
        self.time = self.time.addSecs(self.time_left)
        self.time_label.setText(self.time.toString())


    def update_time_label(self):
        self.time_left -= 1
        self.time = self.time.addSecs(-1)
        self.time_label.setText(self.time.toString())


    def count_down(self):
        self.worker = CountdownThread(self.time_left)
        self.worker.time_signal.update.connect(self.update_time_label)
        self.worker.time_signal.stop.connect(self.reset_timer)
        self.worker.time_signal.finished.connect(self.alarm)
        self.worker.start()


    def alarm(self):
        self.done_btn.setEnabled(True)
        self.start_stop_btn.setEnabled(False)
        self.show_dialog()


    def show_dialog(self):
        dialog = QDialog()
        dialog.setWindowTitle = "Time for your reps!"
        dialog_label = QLabel("Timer abgelaufen!", dialog)
        dialog_button = QPushButton("Ok", dialog)
        dialog_button.clicked.connect(dialog.accept)
        
        vbox = QVBoxLayout(dialog)
        vbox.addWidget(dialog_label)
        vbox.addWidget(dialog_button)
        dialog.setLayout(vbox)
        
        dialog.exec()