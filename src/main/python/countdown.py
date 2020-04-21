from PyQt5.QtCore import QThread, pyqtSignal, QObject
import time

class Worker(QObject):
    update = pyqtSignal()
    stop = pyqtSignal()
    finished = pyqtSignal()


class CountdownThread(QThread):
    def __init__(self, time_left):
        QThread.__init__(self)
        self.time_signal = Worker()
        self.time_left = time_left
        self.is_running = True


    def stop(self):
        self.is_running = False

    
    def run(self):
        while self.is_running:
            self.time_left -= 1
            time.sleep(1)
            self.time_signal.update.emit()
            if self.time_left == 0:
                self.stop()
                self.time_signal.finished.emit()
                return
        
        self.time_signal.stop.emit()