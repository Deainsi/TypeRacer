import time

import essential_generators
from PyQt5 import QtCore, QtWidgets

from Nthread import NThread


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(931, 695)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.seconds = -4
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 941, 701))
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(792, 30, 121, 31))
        self.pushButton.setStyleSheet("QPushButton{background-color: rgb(43, 255, 241);\n"
                                      "border-radius:10px;}\n"
                                      "QPushButton::hover\n"
                                      "{\n"
                                      "background-color:rgb(39, 220, 240)\n"
                                      "}\n"
                                      "QPushButton::pressed\n"
                                      "{\n"
                                      "}\n"
                                      "background-color: rgb(2, 166, 255);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.race_start)
        self.textBrowser = QtWidgets.QTextBrowser(self.frame)
        self.textBrowser.setGeometry(QtCore.QRect(40, 150, 851, 341))
        self.textBrowser.setStyleSheet("background-color: rgb(230, 230, 230);\n"
                                       "border:none;")
        self.textBrowser.setObjectName("textBrowser")
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setGeometry(QtCore.QRect(40, 580, 851, 31))
        self.lineEdit.setStyleSheet("background-color: rgb(230, 230, 230);")
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(440, 290, 51, 71))
        self.label.setStyleSheet("font: 48pt \"MS Shell Dlg 2\";\n"
                                 "background-color:rgb(230,230,230);")
        self.label.setText("")
        self.label.setVisible(False)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(60, 50, 91, 31))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_2.setVisible(False)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(40, 20, 400, 100))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_3.setVisible(False)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Start"))

    def race_start(self):
        paragraph = essential_generators.DocumentGenerator().paragraph()
        self.pushButton.setEnabled(False)
        self.label.setVisible(True)
        self.label_3.setVisible(False)
        self.textBrowser.clear()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.countup)
        self.thread = NThread(self.lineEdit, paragraph, self.textBrowser, self.label, self.label_2)
        self.thread.finished.connect(self.race_finish)
        self.thread.start()
        self.timer.singleShot(3000, self.countup)
        self.timer.start(1000)

    def race_finish(self, mistakes, total, paragraph_length):
        self.timer.stop()
        self.pushButton.setEnabled(True)
        race_time = self.seconds / 60
        stime = (f"00:0{self.seconds}" if self.seconds < 10 else f"00:{self.seconds}") \
            if self.seconds < 60 else (f"{int(self.seconds / 60)}:0{self.seconds % 60}"
                                       if self.seconds % 60 < 10 else f"{int(self.seconds / 60)}:{self.seconds % 60}")
        self.seconds = -4
        self.label_2.setVisible(False)
        wpm = int(paragraph_length / race_time)
        accuracy = f"{total/(total+mistakes)*100:.2f}"
        text = f"Words per minute: {wpm}\n" \
               f"Accuracy: {accuracy}%\n" \
               f"Time: {stime}"
        self.label_3.setVisible(True)
        self.label_3.setText(text)

    def countup(self):
        self.seconds += 1
        stime = (f"00:0{self.seconds}" if self.seconds < 10 else f"00:{self.seconds}") \
            if self.seconds < 60 else (f"{int(self.seconds / 60)}:0{self.seconds % 60}"
            if self.seconds % 60 < 10 else f"{int(self.seconds / 60)}:{self.seconds % 60}")
        self.label_2.setText(stime)
