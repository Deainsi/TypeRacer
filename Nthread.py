import time

from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QColor


class NThread(QThread):
    counter = 0
    mistakes = 0
    finished = pyqtSignal(int,int, int)
    red = QColor(255, 0, 0)
    black = QColor(0, 0, 0)

    def __init__(self, le, text, tb, lb, tlb):
        QThread.__init__(self)
        self.le = le
        self.tb = tb
        self.paragraph = text.split()
        self.lb = lb
        self.tlb = tlb

    def run(self):
        for i in reversed(range(1, 4)):
            self.lb.setText(str(i))
            time.sleep(1)
        self.lb.setVisible(False)
        self.tlb.setVisible(True)
        self.tb.setTextColor(self.red)
        self.tb.append(self.paragraph[0] + " ")
        self.tb.setTextColor(self.black)
        self.tb.insertPlainText(" ".join(self.paragraph[1:]))
        self.le.textEdited.connect(self.checker)

    def checker(self):
        text = self.le.text()
        if text != self.paragraph[self.counter]:
            if text != self.paragraph[self.counter][:len(text)]:
                self.le.setStyleSheet("QLineEdit{background-color:rgb(200,0,0);}")
                self.mistakes += 1
            else:
                self.le.setStyleSheet("QLineEdit{background-color:rgb(230,230,230);}")
        else:
            self.le.setText("")
            self.counter += 1
            if self.counter != len(self.paragraph):
                self.tb.clear()
                self.tb.insertPlainText(" ".join(self.paragraph[:self.counter]))
                self.tb.setTextColor(self.red)
                self.tb.insertPlainText(" " + self.paragraph[self.counter] + " ")
                self.tb.setTextColor(self.black)
                self.tb.insertPlainText(" ".join(self.paragraph[self.counter + 1:]))
            else:
                self.tb.clear()
                self.tb.insertPlainText(" ".join(self.paragraph))
                self.finished.emit(self.mistakes, sum([len(i) for i in self.paragraph]), len(self.paragraph))


