from PyQt5 import QtWidgets, QtCore, QtGui
from mainwindow import Ui_MainWindow
import sys
import socket
import threading
import errno
import time
connected = True


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
        
        
        # * DEFINING STANDARDS OF THE TCP STREAM CLIENT SOCKET CONNECTION
        self.HEADER = 64  # * Define a constant size of the header
        self.PORT = 5050  # * Define a port for the socket that client access
        self.FORMAT = 'utf-8'  # * A decoding/encoding format of the messages
        self.DISCONNECT_MESSAGE = '!DISCONNECT'  # * A defined disconnect message
        self.connected = True
        
        # * Define the IPv4 address the client will connect to.
        self.SERVER = socket.gethostbyname(socket.gethostname())
        
        
        # * The address to which the client will connect
        self.ADDRESS = (self.SERVER, self.PORT)
        self.idle_status = False
        self.status = ""
        
        
        # * defining a socket object for the client
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        
        # * connecting the client socket to the server socket
        self.client.connect(self.ADDRESS)
        self.timer = QtCore.QTimer(self)

        # * adding action to timer
        self.timer.timeout.connect(self.check_timeout)

        # * update the timer every tenth second
        self.timer.start(100)

        # * execute client handling in a new thread
        self.thread = threading.Thread(target=self.recieve_status_message)
        self.thread.start()

    def recieve_status_message(self):
        global connected
        while connected:
            # * recieve the length of the status message sent from the server
            try:
                try:
                    status_length = int(self.client.recv(self.HEADER).decode(self.FORMAT))
                except ValueError:
                    print("[FINISHED] Connection ended due to achieving required result ...")
                    connected = False
                # * recieve the status message itself from the server
                self.status = self.client.recv(status_length).decode(self.FORMAT)
                print(self.status)
                if self.status == self.DISCONNECT_MESSAGE:
                    self.idle_status = True
                    connected = False
            except ConnectionAbortedError:
                print("[EXITING] The GUI was closed ... ")
        self.client.close()
        print("[EXITING] Exiting recieving thread .. ")
        sys.exit()
        

        

    def answer_question(self, answer):
        global connected
        if not self.idle_status:
            if self.questionIndex < 9:
                message = answer.encode(self.FORMAT)  # * encode the message
                msg_length = f"{len(message):<{self.HEADER}}".encode(self.FORMAT)  # * create the header of the message
                self.client.send(msg_length)  # * send the header first
                self.client.send(message)  # * send the message
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
                    self.ui.Question.setText(
                        self.questions[self.questionIndex])

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
                        
                        finished_message = f"{len(self.DISCONNECT_MESSAGE):<{self.HEADER}}" + self.DISCONNECT_MESSAGE
                        self.client.send(finished_message.encode(self.FORMAT))
                        connected = False

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
                        self.ui.Question.setText(
                            self.questions[self.questionIndex])
                        self.answers = []
                    
                    
                else:
                    time.sleep(1)
                    diagnosis = self.diagnosis_detection()
                    item = QtWidgets.QTableWidgetItem("Auto Doctor:   " + diagnosis)
                    self.ui.Question.setText(diagnosis)
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.ui.Chat.setItem(self.questionIndex*2, 0, item)
                    self.ui.Yes.setText("Okay, thank you Dr.")
                    self.ui.No.setText("I want to answer the questions again.")

    def diagnosis_detection(self):
        print(self.answers)
        return self.status

    def check_timeout(self):
        if self.idle_status:
            QtWidgets.QMessageBox.about(
                self, "Connection Lost", "[IDLE] Connection was closed please open the UI again")
            sys.exit()

    def closeEvent(self, event):
        global connected
        print("[EXITING] ... ")
        connected = False
        if connected:
            finished_message = f"{len(self.DISCONNECT_MESSAGE):<{self.HEADER}}" + self.DISCONNECT_MESSAGE
            self.client.send(finished_message.encode(self.FORMAT))
        self.client.close()
        time.sleep(1)

        


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()
