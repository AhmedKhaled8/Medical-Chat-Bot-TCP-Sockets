from PyQt5 import QtWidgets, QtCore, QtGui
from mainwindow import Ui_MainWindow
import sys


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.questions = ['Do you have a cough?', 'Do you have a fever?', 'Do you have shortness of breath?',
                          'Are you experiencing any fatigue?', 'Do you have a sore throat?', 'Do you have a runny nose?',
                          'Do you have any muscle pain?', 'Do you have a headache?', 'Are you experiencing loss of taste or smell?']

        self.questionIndex = 0
        self.ui.Question.setText(self.questions[self.questionIndex])
        self.answers = []
        self.ui.Yes.clicked.connect(lambda: self.answer_question("Yes"))
        self.ui.No.clicked.connect(lambda: self.answer_question("No"))


    def answer_question(self, answer):
        if self.questionIndex < 9:
            self.answers.append(answer)
            item = QtWidgets.QTableWidgetItem(
                "Auto Doctor:   " + str(self.questions[self.questionIndex]))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.Chat.setItem(self.questionIndex*2, 0, item)
            item = QtWidgets.QTableWidgetItem(
                str(self.answers[self.questionIndex]) + "   :You")
            item.setTextAlignment(QtCore.Qt.AlignRight)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.Chat.setItem(self.questionIndex*2+1, 1, item)
            self.questionIndex += 1
            if self.questionIndex < 9:
                self.ui.Question.setText(self.questions[self.questionIndex])

        if self.questionIndex == 9:
            if self.ui.Yes.text() == "Okay, thank you Dr.":
                if answer == "Yes":
                    item = QtWidgets.QTableWidgetItem(
                        self.ui.Yes.text() + "   :You")
                    item.setTextAlignment(QtCore.Qt.AlignRight)
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.ui.Chat.setItem(self.questionIndex*2+1, 1, item)
                    self.ui.Yes.setText("")
                    self.ui.No.setText("")
                    self.ui.Question.setText("")
                    self.questionIndex += 1
                else:
                    for i in range(self.questionIndex+1):
                        item = QtWidgets.QTableWidgetItem("")
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.ui.Chat.setItem(i*2, 0, item)
                        item = QtWidgets.QTableWidgetItem("")
                        item.setTextAlignment(QtCore.Qt.AlignRight)
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.ui.Chat.setItem(
                            i*2+1, 1, item)

                    self.questionIndex = 0
                    self.ui.Yes.setText("Yes")
                    self.ui.No.setText("No")
                    self.ui.Question.setText(self.questions[self.questionIndex])
                    self.answers = []

            else:
                diagoses = self.diagoses_detection(self.answers)
                item = QtWidgets.QTableWidgetItem(
                    "Auto Doctor:   " + diagoses)
                self.ui.Question.setText(diagoses)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.ui.Chat.setItem(self.questionIndex*2, 0, item)
                self.ui.Yes.setText("Okay, thank you Dr.")
                self.ui.No.setText("I want to answer the questions again.")

    def diagoses_detection(self, answers_list):
        print(self.answers)
        diagoses = "Your predicted diagoses is ....."
        return diagoses


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()
